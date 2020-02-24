# Codalab Bundle

This folder contains the necesary files to replicate the competition at Codalab.
We made our best to automate this process, but since Codalab has some configuration options that cannot be
automatically setup in the `competition.yaml`, some manual configuration is still necesary.

1. Run `make codalab` to create the `codalab/codalab.zip` competition bundle file.
2. Create a new competition in Codalab and upload the bundle zip file.
3. Edit the competition and set the value of `Competition docker image` to `codalab/codalab-legacy:py3`.

Finally, run `make baseline` and submit the `baseline.zip` file to verify that everything, hopefully, worked.

## Things that must be manually configured in Codalab

- `Competition docker image`
- `Allow teams`
- `Enable per submission metadata`
- `Leaderboard mode: Hide results` (for Testing phase)
- All the text on the overview, data, terms, and evaluation pages
