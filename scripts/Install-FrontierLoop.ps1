[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Source,
  [Parameter(Mandatory)][string]$DestinationRoot,
  [string]$UserSkillRoot,
  [string[]]$MarketplaceFiles=@(),
  [switch]$WhatIf,
  [switch]$InjectFailureAfterSwap
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function Full([string]$P){[IO.Path]::GetFullPath($P).TrimEnd([char[]]'\/')}
function Child([string]$P,[string]$R){(Full $P).StartsWith((Full $R)+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)}
function Excluded([string]$Rel){$p=$Rel.Replace('\','/').ToLowerInvariant();$p.StartsWith('evaluation/results/')-or$p.Contains('/__pycache__/')-or$p.EndsWith('.pyc')-or$p.Contains('/.frontier-loop-')-or$p.Contains('install-backup')-or$p.Contains('/temp/')}
function Inventory([string]$Base){
  $r=Full $Base;$rows=[Collections.Generic.List[object]]::new();$stack=[Collections.Generic.Stack[string]]::new();$stack.Push($r)
  while($stack.Count){$d=$stack.Pop();foreach($i in [IO.DirectoryInfo]::new($d).EnumerateFileSystemInfos()|Sort-Object FullName){$rel=[IO.Path]::GetRelativePath($r,$i.FullName).Replace('\','/');if(Excluded $rel){continue};$rp=(($i.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0);if($rp){$rows.Add([ordered]@{path=$rel;kind='reparse';target=[string](@($i.Target)[0])})}elseif($i-is[IO.DirectoryInfo]){$stack.Push($i.FullName)}else{$rows.Add([ordered]@{path=$rel;kind='file';length=$i.Length;sha256=(Get-FileHash -LiteralPath $i.FullName -Algorithm SHA256).Hash})}}}
  @($rows|Sort-Object path,kind)
}
function SameTree([string]$A,[string]$B){(ConvertTo-Json -InputObject @(Inventory $A) -Compress -Depth 6)-eq(ConvertTo-Json -InputObject @(Inventory $B) -Compress -Depth 6)}
function CopyTree([string]$From,[string]$To){[IO.Directory]::CreateDirectory($To)|Out-Null;foreach($r in @(Inventory $From)){if($r.kind-ne'file'){if($r.kind-eq'reparse'){throw "Source reparse entry rejected: $($r.path)"};continue};$src=Join-Path $From $r.path;$dst=Join-Path $To $r.path;[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dst))|Out-Null;[IO.File]::Copy($src,$dst,$false)}}
function LinkTarget($Item){$t=[string](@($Item.Target)[0]);if(-not[IO.Path]::IsPathRooted($t)){$t=Join-Path $Item.Parent.FullName $t};Full $t}
function RemoveNode([string]$Path){
  if(-not(Test-Path -LiteralPath $Path)){return}
  $i=Get-Item -LiteralPath $Path -Force
  if(($i.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0){Remove-Item -LiteralPath $Path -Force;return}
  if($i-is[IO.DirectoryInfo]){[IO.Directory]::Delete($i.FullName,$true);return}
  throw "Refusing to remove unexpected non-directory install node: $Path"
}
function IsRecognizedManagedJunction([string]$Target,[string]$SkillName,[string]$SourceSkill,[string]$VersionRoot){
  if([string]::Equals((Full $Target),(Full $SourceSkill),[StringComparison]::OrdinalIgnoreCase)){return $true}
  if(-not(Child $Target $VersionRoot)){return $false}
  $relative=[IO.Path]::GetRelativePath($VersionRoot,(Full $Target))
  $parts=@($relative-split '[\\/]')
  $semver='^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$'
  return $parts.Count-eq3-and$parts[0]-match$semver-and$parts[1]-eq'skills'-and$parts[2]-eq$SkillName
}
function FindManagedMaterializedSource([string]$Path,[string]$SkillName,[string]$VersionRoot){
  if(-not(Test-Path -LiteralPath $VersionRoot -PathType Container)){return $null}
  $semver='^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$'
  foreach($v in @(Get-ChildItem -LiteralPath $VersionRoot -Directory -Force|Where-Object Name -Match $semver|Sort-Object Name -Descending)){
    $candidate=Join-Path $v.FullName "skills\$SkillName"
    if(Test-Path -LiteralPath $candidate -PathType Container){
      $ci=Get-Item -LiteralPath $candidate -Force
      if(($ci.Attributes-band[IO.FileAttributes]::ReparsePoint)-eq0-and(SameTree $Path $candidate)){return (Full $candidate)}
    }
  }
  return $null
}
function Assert-SoleRegisteredPlugin([string[]]$Files,[string]$ExpectedSource){
  if(-not$Files.Count){return}
  $total=0
  foreach($file in $Files){
    $marketplace=Full $file;$data=Get-Content -LiteralPath $marketplace -Raw|ConvertFrom-Json
    $matches=@($data.plugins|Where-Object name -eq 'frontier-loop');$count=$matches.Count
    if($count-ne1){throw "Marketplace must contain exactly one frontier-loop registration: $file ($count)"}
    $total+=$count
    $source=$matches[0].source
    if(-not$source-or[string]$source.source-ne'local'-or[string]::IsNullOrWhiteSpace([string]$source.path)){throw "FrontierLoop marketplace source must be a local path: $file"}
    $declared=[string]$source.path
    $resolved=if([IO.Path]::IsPathRooted($declared)){Full $declared}else{Full (Join-Path ([IO.Path]::GetDirectoryName($marketplace)) $declared)}
    if(-not[string]::Equals($resolved,(Full $ExpectedSource),[StringComparison]::OrdinalIgnoreCase)){throw "FrontierLoop marketplace source differs from canonical source: $file -> $resolved"}
  }
  if($total-ne1){throw "Multiple effective frontier-loop registrations across supplied marketplaces: $total"}
}

$Source=Full $Source
$DestinationRoot=Full $DestinationRoot
if($UserSkillRoot){$UserSkillRoot=Full $UserSkillRoot}
Assert-SoleRegisteredPlugin $MarketplaceFiles $Source
$verify=Join-Path $Source 'scripts\Verify-FrontierLoop.ps1'
& $verify -Root $Source|Out-Null
if($LASTEXITCODE-ne0){throw 'Source verification failed'}
$version=[string]((Get-Content -LiteralPath (Join-Path $Source '.codex-plugin\plugin.json')-Raw|ConvertFrom-Json).version)
$destination=Join-Path $DestinationRoot $version
$skills=@(Get-ChildItem -LiteralPath (Join-Path $Source 'skills')-Directory|Where-Object {Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')}|Sort-Object Name)
$plan=[Collections.Generic.List[object]]::new()
if($UserSkillRoot){foreach($s in $skills){
  $dst=Join-Path $UserSkillRoot $s.Name
  $target=Join-Path $destination "skills\$($s.Name)"
  $sourceSkill=Join-Path $Source "skills\$($s.Name)"
  if(-not(Test-Path -LiteralPath $dst)){$plan.Add([ordered]@{name=$s.Name;path=$dst;target=$target;action='created-materialized';previousKind='missing';previousTarget=$null});continue}
  $i=Get-Item -LiteralPath $dst -Force
  $rp=(($i.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0)
  if($rp){
    if($i.LinkType-ne'Junction'){throw "Conflicting skill link: $($s.Name)"}
    $current=LinkTarget $i
    if(-not(IsRecognizedManagedJunction $current $s.Name $sourceSkill $DestinationRoot)){throw "Conflicting skill link: $($s.Name)"}
    $plan.Add([ordered]@{name=$s.Name;path=$dst;target=$target;action='materialize-managed-junction';previousKind='junction';previousTarget=$current})
  }elseif(-not($i-is[IO.DirectoryInfo])){throw "Conflicting skill file: $($s.Name)"}
  elseif(@(Get-ChildItem -LiteralPath $dst -Force).Count-eq0){$plan.Add([ordered]@{name=$s.Name;path=$dst;target=$target;action='replace-empty';previousKind='directory';previousTarget=$null})}
  elseif(SameTree $dst $sourceSkill){$plan.Add([ordered]@{name=$s.Name;path=$dst;target=$target;action='unchanged-source-materialized';previousKind='directory';previousTarget=$null})}
  else{
    $managed=FindManagedMaterializedSource $dst $s.Name $DestinationRoot
    if($managed){$plan.Add([ordered]@{name=$s.Name;path=$dst;target=$target;action='upgrade-materialized-version';previousKind='directory';previousTarget=$managed})}
    else{throw "Conflicting skill directory: $($s.Name)"}
  }
}}
if($WhatIf){[ordered]@{success=$true;whatIf=$true;version=$version;destination=$destination;userSkillInstallMode='materialized-copy';skillActions=$plan;rollback='NotNeeded'}|ConvertTo-Json -Depth 6;exit 0}

$id=[guid]::NewGuid().ToString('N')
$stage=Join-Path $DestinationRoot ".frontier-loop-staging-$id"
$destBackup=Join-Path $DestinationRoot ".frontier-loop-install-backup-$id"
$skillBackups=[Collections.Generic.List[object]]::new()
$createdSkills=[Collections.Generic.List[string]]::new()
$swapped=$false
$hadDestination=Test-Path -LiteralPath $destination
$idempotent=$false
try{
  [IO.Directory]::CreateDirectory($DestinationRoot)|Out-Null
  CopyTree $Source $stage
  & $verify -Root $stage -ExpectedSource $Source|Out-Null
  if($LASTEXITCODE-ne0){throw 'Staging verification failed'}
  if($hadDestination-and(SameTree $destination $Source)){$idempotent=$true;[IO.Directory]::Delete($stage,$true)}else{if($hadDestination){Move-Item -LiteralPath $destination -Destination $destBackup};Move-Item -LiteralPath $stage -Destination $destination;$swapped=$true}
  if($UserSkillRoot){
    [IO.Directory]::CreateDirectory($UserSkillRoot)|Out-Null
    foreach($p in $plan){
      if($p.action-eq'unchanged-source-materialized'){continue}
      if(Test-Path -LiteralPath $p.path){$backup=Join-Path $UserSkillRoot ".frontier-loop-install-backup-$id-$($p.name)";Move-Item -LiteralPath $p.path -Destination $backup;$skillBackups.Add([ordered]@{path=$p.path;backup=$backup;previousKind=$p.previousKind;previousTarget=$p.previousTarget;action=$p.action})}
      CopyTree $p.target $p.path
      $createdSkills.Add($p.path)
    }
  }
  if($InjectFailureAfterSwap){throw 'Injected failure after swap'}
  & $verify -Root $destination -ExpectedSource $Source|Out-Null
  if($LASTEXITCODE-ne0){throw 'Destination verification failed'}
  foreach($p in $plan){$i=Get-Item -LiteralPath $p.path -Force;if(($i.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0-or-not($i-is[IO.DirectoryInfo])-or-not(SameTree $p.path $p.target)){throw "Installed materialized skill verification failed: $($p.name)"}}
  foreach($b in $skillBackups){if(Test-Path -LiteralPath $b.backup){RemoveNode $b.backup}}
  if(Test-Path -LiteralPath $destBackup){[IO.Directory]::Delete($destBackup,$true)}
  [ordered]@{success=$true;whatIf=$false;version=$version;destination=$destination;idempotent=$idempotent;userSkillInstallMode='materialized-copy';skillActions=$plan;rollback='NotNeeded'}|ConvertTo-Json -Depth 6
  exit 0
}catch{
  [Console]::Error.WriteLine('restoring previous FrontierLoop state')
  foreach($path in @($createdSkills)){if(Test-Path -LiteralPath $path){RemoveNode $path}}
  foreach($b in $skillBackups){if(Test-Path -LiteralPath $b.backup){Move-Item -LiteralPath $b.backup -Destination $b.path;if($b.previousKind-eq'junction'){$restored=Get-Item -LiteralPath $b.path -Force;if($restored.LinkType-ne'Junction'-or-not[string]::Equals((LinkTarget $restored),(Full $b.previousTarget),[StringComparison]::OrdinalIgnoreCase)){throw "Skill junction rollback verification failed: $($b.path)"}}elseif($b.previousKind-eq'directory'){$restored=Get-Item -LiteralPath $b.path -Force;if(($restored.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0-or-not($restored-is[IO.DirectoryInfo])){throw "Skill directory rollback verification failed: $($b.path)"}}}}
  if($swapped-and(Test-Path -LiteralPath $destination)){[IO.Directory]::Delete($destination,$true)}
  if(Test-Path -LiteralPath $destBackup){Move-Item -LiteralPath $destBackup -Destination $destination}
  if(Test-Path -LiteralPath $stage){[IO.Directory]::Delete($stage,$true)}
  throw
}
