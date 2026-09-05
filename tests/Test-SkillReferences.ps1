[CmdletBinding()]
param([string]$Source=(Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference='Stop'
$verify=Join-Path $Source 'scripts/Verify-SkillReferences.ps1'
$temp=Join-Path ([IO.Path]::GetTempPath()) ('skill-reference-test-'+[guid]::NewGuid().ToString('N'))
$root=Join-Path $temp 'skills'
$skill=Join-Path $root 'example'
$passes=[Collections.Generic.List[string]]::new()
function Body([string]$Text){[IO.File]::WriteAllText((Join-Path $skill 'SKILL.md'),$Text,[Text.UTF8Encoding]::new($false))}
function Expect([string]$Name,[bool]$Success){
  $passed=$true
  try{& $verify -SkillRoot $root | Out-Null}catch{$passed=$false}
  if($passed-ne$Success){throw "Unexpected reference result: $Name"}
  $passes.Add($Name)
}
try{
  [IO.Directory]::CreateDirectory((Join-Path $skill 'references'))|Out-Null
  Expect 'empty-tree-rejected' $false
  Body '# Active skill';Expect 'no-links' $true
  [IO.File]::WriteAllText((Join-Path $skill 'references/rule.md'),'# Rule')
  Body '[rule](references/rule.md)';Expect 'local-link' $true
  Body 'Read `references/missing.md`.';Expect 'missing-rejected' $false
  [IO.Directory]::CreateDirectory((Join-Path $temp 'references'))|Out-Null
  [IO.File]::WriteAllText((Join-Path $temp 'references/RUNTIME_BOUNDARY.md'),'# Boundary')
  Body 'Read `../../references/RUNTIME_BOUNDARY.md`.';Expect 'old-ancestor-layout-rejected' $false
  [IO.Directory]::CreateDirectory((Join-Path $root 'frontier-core/references'))|Out-Null
  [IO.File]::WriteAllText((Join-Path $root 'frontier-core/references/RUNTIME_BOUNDARY.md'),'# Boundary')
  Body '[rule](../frontier-core/references/RUNTIME_BOUNDARY.md)';Expect 'portable-core-sibling' $true
  Body '[docs](https://example.invalid/reference.md) [section](#section)';Expect 'external-links-no-network' $true
  $backup=Join-Path $root '.frontier-loop-install-backup-test-example'
  [IO.Directory]::CreateDirectory($backup)|Out-Null
  [IO.File]::WriteAllText((Join-Path $backup 'SKILL.md'),'Read `../../references/old.md`.')
  Expect 'inactive-backup-excluded' $true
  Body '[not-portable](C:/references/rule.md)';Expect 'absolute-path-rejected' $false
  Body '[guide](references/rule.md)'
  [IO.File]::WriteAllText((Join-Path $skill 'references/rule.md'),'[missing](missing.md)')
  Expect 'supporting-document-checked' $false
  [ordered]@{success=$true;count=$passes.Count;tests=@($passes)}|ConvertTo-Json -Compress
}finally{
  if(Test-Path -LiteralPath $temp){[IO.Directory]::Delete($temp,$true)}
}
