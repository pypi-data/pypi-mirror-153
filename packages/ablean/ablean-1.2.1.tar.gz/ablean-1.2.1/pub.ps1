# This API token should be valid for the current $PYPI_REPO and should include the "pypi-" prefix
$PYPI_API_TOKEN = "pypi-AgEIcHlwaS5vcmcCJDY0ODAwMzRhLWJiNjgtNGRkNi05ZWU1LWM2YjY3NDliOWYxNQACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgFBVbtkRL-6EGMe4Ufhf4Ed4kP0N0PQOp_QgApSPZrnY"
# Change to "testpypi" to upload to https://test.pypi.org/
# If you do this, know that PyPI and TestPyPI require different API tokens
$PYPI_REPO="pypi"

function publish_cli
{
    # Push-Location
    # Set-Location $STUBS_DIR
    & conda activate qc38
    & python setup.py --quiet sdist bdist_wheel
    [System.Environment]::SetEnvironmentVariable('TWINE_USERNAME',"__token__")
    [System.Environment]::SetEnvironmentVariable('TWINE_PASSWORD',$PYPI_API_TOKEN)
    [System.Environment]::SetEnvironmentVariable('TWINE_REPOSITORY',$PYPI_REPO)
    & twine upload "dist/*"
    # Pop-Location
}

publish_cli