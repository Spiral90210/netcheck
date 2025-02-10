# netcheck

Raspberry pi based checking tools for your home internet connection.

Licensed under the MIT license - see LICENSE.txt

## Getting Started

You need `nodejs` installed to be able to run this. You have two options - install directly or use (nvm)[https://github.com/nvm-sh/nvm]. I recommend nvm and have a `.nvmrc` file to `nvm use`, but you can install the distro version and just use that, it should be very compatible.

Distro:
```bash
sudo apt-get install -y nodejs
npm install
```

Once you have a nodejs installadion, you can install the project dependencies with `npm`:

```bash
npm install
```

And then run the project with
```bash
npm start
```

It will output the location to bowse to, you can past that into your browser.

By default the server will bind to a random port. If you want to specify a specifc one (recommended if you want to have a browser shortcut to run), then you can `cp .env.example .env` and change the value there.
