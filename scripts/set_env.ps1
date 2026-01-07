param(
  [string]$Path = ".env"
)
if (-not (Test-Path -Path $Path)) { throw "Archivo no encontrado: $Path" }
$lines = Get-Content -Path $Path
foreach ($line in $lines) {
  $trim = $line.Trim()
  if ($trim -eq "") { continue }
  if ($trim.StartsWith("#")) { continue }
  $parts = $trim.Split("=",2)
  if ($parts.Count -ne 2) { continue }
  $name = $parts[0].Trim()
  $value = $parts[1].Trim()
  Set-Item -Path env:$name -Value $value
}
Write-Output "Variables cargadas en la sesión actual."
