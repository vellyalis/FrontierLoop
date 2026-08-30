[CmdletBinding()]
param([string]$Root=(Split-Path $PSScriptRoot -Parent),[string]$ExpectedSource,[string]$JsonOut)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$ExpectedImplicit=@('frontier-architecture','frontier-core','frontier-debug-investigation','frontier-performance-engineering','frontier-portfolio','frontier-recovery','frontier-security-review')|Sort-Object
function Full([string]$P){[IO.Path]::GetFullPath($P).TrimEnd([char[]]'\/')}
function Excluded([string]$Rel){$p=$Rel.Replace('\','/').ToLowerInvariant();return $p-eq'.git'-or$p.StartsWith('.git/')-or$p-eq'provenance'-or$p.StartsWith('provenance/')-or$p.StartsWith('evaluation/results/')-or$p.Contains('/__pycache__/')-or$p.EndsWith('.pyc')-or$p.Contains('/.frontier-loop-')-or$p.Contains('install-backup')-or$p.Contains('/temp/')}
function Require-Patterns([string]$Path,[string[]]$Patterns){
 if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){throw "Missing $Path"}
 $text=Get-Content -LiteralPath $Path -Raw
 foreach($pattern in $Patterns){if($text-notmatch$pattern){throw "Required contract '$pattern' missing from $Path"}}
}
function Inventory([string]$Base){
 $r=Full $Base;$rows=[Collections.Generic.List[object]]::new();$stack=[Collections.Generic.Stack[string]]::new();$stack.Push($r)
 while($stack.Count){$d=$stack.Pop();foreach($i in [IO.DirectoryInfo]::new($d).EnumerateFileSystemInfos()|Sort-Object FullName){$rel=[IO.Path]::GetRelativePath($r,$i.FullName).Replace('\','/');if(Excluded $rel){continue};$rp=(($i.Attributes-band[IO.FileAttributes]::ReparsePoint)-ne0);if($rp){$rows.Add([ordered]@{path=$rel;kind='reparse';target=[string](@($i.Target)[0])})}elseif($i-is[IO.DirectoryInfo]){$stack.Push($i.FullName)}else{$stream=$i.OpenRead();try{$null=$stream.ReadByte()}finally{$stream.Dispose()};$rows.Add([ordered]@{path=$rel;kind='file';length=$i.Length;sha256=(Get-FileHash -LiteralPath $i.FullName -Algorithm SHA256).Hash})}}}
 @($rows|Sort-Object path,kind)
}
try{
 $Root=Full $Root;if(-not(Test-Path -LiteralPath $Root -PathType Container)){throw 'Root missing'}
 $manifestPath=Join-Path $Root '.codex-plugin\plugin.json';if(-not(Test-Path -LiteralPath $manifestPath -PathType Leaf)){throw 'Missing .codex-plugin/plugin.json'}
 $manifest=Get-Content -LiteralPath $manifestPath -Raw|ConvertFrom-Json;if([string]::IsNullOrWhiteSpace([string]$manifest.version)){throw 'Manifest version missing'}
 $taddkorroManifestPath=Join-Path $Root 'taddkorro.plugin.json';if(-not(Test-Path -LiteralPath $taddkorroManifestPath -PathType Leaf)){throw 'Missing taddkorro.plugin.json'}
 $taddkorroManifest=Get-Content -LiteralPath $taddkorroManifestPath -Raw|ConvertFrom-Json
 if($taddkorroManifest.schemaVersion-ne1-or$taddkorroManifest.name-ne'frontier-loop'-or$taddkorroManifest.version-ne$manifest.version-or-not$taddkorroManifest.enabled){throw 'Taddkorro manifest mismatch'}
 if(@($taddkorroManifest.skills).Count-ne1-or$taddkorroManifest.skills[0]-ne'skills'){throw 'Taddkorro Skill root mismatch'}
 $doctrinePath=Join-Path $Root 'skills\frontier-core\references\ENGINEERING_JUDGMENT.md'
 Require-Patterns $doctrinePath @('(?m)^## FOUNDATION\s*$','(?m)^## REDUCTION\s*$','(?m)^## REALITY\s*$','(?m)^## Mechanism admission rule\s*$','DIRECT.*INVESTIGATE.*RESTRUCTURE.*BLOCKED','fixed weights','Do not load this reference for a mechanical micro-edit')
 $wiring=[ordered]@{
  'skills\frontier-core\SKILL.md'=@('references/ENGINEERING_JUDGMENT\.md','conditional decision reference','Routine\s+local edits direct','Do not open .*ENGINEERING_JUDGMENT\.md.*merely to\s+confirm','only after a positive material trigger','module or Core placement','material Module/Core placement')
  'skills\frontier-architecture\SKILL.md'=@('\.\./frontier-core/references/ENGINEERING_JUDGMENT\.md','FOUNDATION','REDUCTION')
  'skills\frontier-debug-investigation\SKILL.md'=@('\.\./frontier-core/references/ENGINEERING_JUDGMENT\.md','INVESTIGATE','compensating mechanism')
  'skills\frontier-performance-engineering\SKILL.md'=@('\.\./frontier-core/references/ENGINEERING_JUDGMENT\.md','For every measured performance goal or regression','before the final engineering decision','mechanism admission rule','authoritative event, direct read, or on-demand action')
  'skills\frontier-migration\SKILL.md'=@('\.\./frontier-core/references/ENGINEERING_JUDGMENT\.md','one canonical\s+authority during coexistence','unbounded dual paths')
 'references\ROUTING_MATRIX.md'=@('ENGINEERING_JUDGMENT\.md','not an eighth implicit Skill','Mechanical micro-edits do\s+not load it')
 }
 foreach($entry in $wiring.GetEnumerator()){Require-Patterns (Join-Path $Root $entry.Key) $entry.Value}
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('specialists supplement frontier-core and never replace','actually read the canonical Engineering Judgment reference before the final engineering decision','trigger list below is mandatory')
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('Do not auto-load the explicit-only.*frontier-complexity-review','obvious speculative complexity')
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('any decision to promote feature behavior into Core','do not load frontier-portfolio or frontier-complexity-review')
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('Do not multiply specialists from vocabulary overlap','do not add .*frontier-architecture','merely because persistence or storage is involved','future interruption-safety','unless an actual interruption')
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('narrow performance mechanism replacement is not automatically an Architecture Workstream','Architecture is optional rather than mandatory')
 Require-Patterns (Join-Path $Root 'skills\frontier-debug-investigation\SKILL.md') @('race, timing, shutdown, cancellation, ordering, or lifetime defect','investigation decision itself','positive concurrency/lifetime trigger')
 Require-Patterns (Join-Path $Root 'skills\frontier-architecture\SKILL.md') @('Core-versus-feature placement is always a positive Doctrine-read trigger','explicit frontier-migration already owns coexistence')
 Require-Patterns (Join-Path $Root 'skills\frontier-migration\SKILL.md') @('not merely because the migrated surface is persisted','add frontier-recovery only after an actual interruption')
 Require-Patterns (Join-Path $Root 'skills\frontier-recovery\SKILL.md') @('only after an actual interruption','Do not auto-load this Skill merely because a design or migration must be interruption-safe','design-time responsibility')
 Require-Patterns (Join-Path $Root 'skills\frontier-architecture\SKILL.md') @('obvious speculative Core promotion can be rejected directly','Do not load the\s+explicit-only `frontier-complexity-review`')
 Require-Patterns (Join-Path $Root 'skills\frontier-core\SKILL.md') @('positive activation contract','actually open and read every matching specialist','reading only .*ENGINEERING_JUDGMENT\.md.*does not satisfy specialist activation','independent triggers coexist')
 foreach($name in @('frontier-architecture','frontier-debug-investigation','frontier-security-review','frontier-performance-engineering')){Require-Patterns (Join-Path $Root ('skills\'+$name+'\SKILL.md')) @('alongside frontier-core','supplements and never replaces frontier-core')}
 Require-Patterns (Join-Path $Root 'skills\frontier-routine-change\SKILL.md') @('Routine or micro-edit user request is NOT itself a trigger','never auto-select this Skill','never load it as a peer to an implicit specialist','never use it to replace frontier-core')
 Require-Patterns (Join-Path $Root 'scripts\Install-FrontierLoop.ps1') @("userSkillInstallMode='materialized-copy'",'materialize-managed-junction','Installed materialized skill verification failed','Conflicting skill directory','marketplace source differs from canonical source')
 Require-Patterns (Join-Path $Root 'tests\Test-FrontierLoopInstall.ps1') @('install-materialized','materialized-doctrine-resolution','source-junction-materialized','prior-materialized-upgrade','foreign-directory-fail-closed','marketplace-canonical-source','marketplace-wrong-source-fail-closed')
 if(-not$ExpectedSource){
  Require-Patterns (Join-Path $Root 'provenance\vibe-harness-devkit-0.3.2-draft\README.md') @('developer-only provenance','Git tag `v0\.8\.2`','SKILL_SOURCE_MAP\.json')
  Require-Patterns (Join-Path $Root 'THIRD_PARTY_NOTICES.md') @('release archives exclude developer-only `provenance/`','Git tag `v0\.8\.2`')
 }
 $skillRoot=Join-Path $Root 'skills';$skills=@(Get-ChildItem -LiteralPath $skillRoot -Directory -Force|Where-Object {Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf}|Sort-Object Name);if($skills.Count-ne23){throw "Skill count $($skills.Count) != 23"}
 $implicit=[Collections.Generic.List[string]]::new()
 foreach($s in $skills){$text=Get-Content -LiteralPath (Join-Path $s.FullName 'SKILL.md') -Raw;$fm=[regex]::Match($text,'(?s)\A---\r?\n(.*?)\r?\n---\r?\n');$nm=[regex]::Matches($fm.Groups[1].Value,'(?m)^name:\s*([^\r\n]+)\s*$');if(-not$fm.Success-or$nm.Count-ne1-or$nm[0].Groups[1].Value.Trim(' ','"',"'")-ne$s.Name){throw "Skill frontmatter mismatch: $($s.Name)"};$yp=Join-Path $s.FullName 'agents\openai.yaml';if(-not(Test-Path -LiteralPath $yp -PathType Leaf)){throw "Missing openai.yaml: $($s.Name)"};$ym=[regex]::Matches((Get-Content -LiteralPath $yp -Raw),'(?mi)^\s*allow_implicit_invocation:\s*(true|false)\s*$');if($ym.Count-ne1){throw "Implicit policy malformed: $($s.Name)"};if([bool]::Parse($ym[0].Groups[1].Value)){$implicit.Add($s.Name)}}
 $actual=@($implicit|Sort-Object);if(@(Compare-Object $ExpectedImplicit $actual).Count){throw "Implicit set mismatch: $($actual-join',')"}
 $sourceMapPath=Join-Path $Root 'references\SKILL_SOURCE_MAP.json';if(-not(Test-Path -LiteralPath $sourceMapPath -PathType Leaf)){throw 'Missing references/SKILL_SOURCE_MAP.json'}
 $sourceMap=Get-Content -LiteralPath $sourceMapPath -Raw|ConvertFrom-Json;if([string]$sourceMap.frontierloop_version-ne[string]$manifest.version){throw 'SKILL_SOURCE_MAP version differs from plugin manifest'}
 foreach($row in @($sourceMap.skills)){$active=Join-Path $skillRoot ([string]$row.active_name+'\SKILL.md');if(-not(Test-Path -LiteralPath $active -PathType Leaf)){throw "Mapped active Skill missing: $($row.active_name)"};$hash=(Get-FileHash -LiteralPath $active -Algorithm SHA256).Hash;if($hash-ne[string]$row.active_sha256){throw "Mapped active Skill hash drift: $($row.active_name)"}}
 $inventory=@(Inventory $Root);if($ExpectedSource){$source=@(Inventory (Full $ExpectedSource));if((ConvertTo-Json $inventory -Compress -Depth 6)-ne(ConvertTo-Json $source -Compress -Depth 6)){throw 'ExpectedSource file drift detected'}}
 $result=[ordered]@{success=$true;root=$Root;version=[string]$manifest.version;skillCount=$skills.Count;implicitCount=$actual.Count;explicitCount=$skills.Count-$actual.Count;implicitNames=$actual;fileCount=@($inventory|Where-Object kind -eq 'file').Count}
 $json=$result|ConvertTo-Json -Depth 6;if($JsonOut){[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName((Full $JsonOut)))|Out-Null;[IO.File]::WriteAllText((Full $JsonOut),$json+[Environment]::NewLine,[Text.UTF8Encoding]::new($false))};$json;exit 0
}catch{[Console]::Error.WriteLine($_.Exception.Message);exit 1}
