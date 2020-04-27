# netcheck

Raspberry pi based checking tools for your home internet connection.

Licensed under the MIT license - see LICENSE.txt

## Getting Started

This is python based, recommend using a virtual environment. The gitignore file is setup for a `.venv` folder so you can execute the following to set it up:

```bash
# Install nodejs dependency on one of the testers (fast.com)
npm install --global fast-cli

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This will set up a python virtual environment and start using it, as well as installing any required dependencies. Python 3.7+ is recommended. There's also a dependency on the nodejs `fast`, but I'm hooting to make that optional in the future. I tried at least one pything version, but it diddn't work and I want to move on rather than get stuck in that particular detail!
