[CmdletBinding()]
param([Parameter(Mandatory)][string]$SkillRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

# Validate the actual materialized topology using the installer's existing
# PowerShell dependency. Transaction backups are not active catalog entries.
if(-not(Test-Path -LiteralPath $SkillRoot -PathType Container)){throw "Skill root missing: $SkillRoot"}
$root=[IO.Path]::GetFullPath($SkillRoot).TrimEnd([char[]]'\/')
$prefix=$root+[IO.Path]::DirectorySeparatorChar
$entries=@(Get-ChildItem -LiteralPath $root -Directory | Where-Object {
  -not $_.Name.StartsWith('.') -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf)
})
if(-not$entries.Count){throw "No Skill entrypoints under: $root"}
$failures=[Collections.Generic.List[object]]::new()
$count=0
$pattern='\]\(([^)\s]+)\)|`((?:\.\./|\./|references/|templates/|schema/)[^`\s]+\.(?:md|json|yaml))`'
foreach($entry in $entries){
  foreach($file in @(Get-ChildItem -LiteralPath $entry.FullName -Recurse -File -Filter '*.md')){
    $text=Get-Content -LiteralPath $file.FullName -Raw -Encoding utf8
    if(-not$text){continue}
    foreach($match in [regex]::Matches($text,$pattern)){
      $target=if($match.Groups[1].Success){$match.Groups[1].Value}else{$match.Groups[2].Value}
      $target=$target.Split('#')[0]
      if(-not$target-or$target.Contains('*')-or$target-match'^(?:https?|mailto):'){continue}
      $count++
      $absolute=[IO.Path]::IsPathRooted($target)-or$target-match'^[A-Za-z]:'
      $resolved=if($absolute){$target}else{[IO.Path]::GetFullPath((Join-Path $file.DirectoryName $target))}
      $outside=$absolute-or-not$resolved.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase)
      if($outside-or-not(Test-Path -LiteralPath $resolved -PathType Leaf)){
        $failures.Add([ordered]@{file=[IO.Path]::GetRelativePath($root,$file.FullName);target=$target;reason=$(if($outside){'outside-skill-tree'}else{'missing'})})
      }
    }
  }
}
if($failures.Count){throw ('Skill reference resolution failed: '+(ConvertTo-Json -InputObject @($failures) -Compress))}
[ordered]@{success=$true;skillCount=$entries.Count;checkedReferences=$count;failures=@()}|ConvertTo-Json -Compress
