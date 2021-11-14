# Dependency Combobulator
![BHEU BADGE](docs/bheu21.svg) ![python](https://img.shields.io/badge/Python-14354C) ![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

Dependency Combobulator is an Open-Source, modular and extensible framework to detect and prevent dependency confusion leakage and potential attacks. This facilitates a holistic approach for ensuring secure application releases that can be evaluated against different sources (e.g., GitHub Packages, JFrog Artifactory) and many package management schemes (e.g., ndm, maven).

### Intendend Audiances

The framework can be used by security auditors, pentesters and even baked into an enterprise's application security program and release cycle in an automated fashion.
### Main features
* Pluggable - interject on commit level, build, release steps in SDLC.
* Expandable - easily add your own package management scheme or code source of choice
* General-purpose Heuristic-Engine - an abstract package data model provides agnostic heuristic approach
* Supporting wide range of technologies
* Flexible - decision trees can be determined upon insights or verdicts provided by the toolkit


### Easly exstensible

The project is putting practicionar's ability to extend and fit the toolkit to her own specific needs. As such, it is designed to be able to extend it to other sources, public registries, package management schemes and extending the abstract model and accompnaied heuristics engine.


## Installation

Dependency Combobulator is ready to work with as it is - just `git clone` or download the package from https://github.com/apiiro/combobulator

Make sure to install required dependencies by running:

`python3 -m pip install python-dotenv gql argparse`

## Arguments (--help)
```
  -h, --help            show this help message and exit
  -t {npm,NuGet,maven}, --type {npm,NuGet,maven}
                        Package Manager Type, i.e: npm, NuGet, maven
  -l LIST_FROM_FILE, --load_list LIST_FROM_FILE
                        Load list of dependencies from a file
  -d FROM_SRC, --directory FROM_SRC
                        Extract dependencies from local source repository
  -p--package SINGLE    Name a single package.
  -c CSV, --csv CSV     Export packages properties onto CSV file
  -gh GITHUB_TOKEN, --github GITHUB_TOKEN
                        GitHub Access Token (Overrides .env file setting)
  -a {compare,comp,heuristics,heur}, --analysis {compare,comp,heuristics,heur}
                        Required analysis level - compare (comp), heuristics
                        (heur) (default: compare)

Apiiro <Heart> Community
```
Supported package types (-t, --t): npm, maven

Supported source dependency assessment:
- From file containing the dependency identifiers line-by-line. (-l, --load_list)
- By analyzing the appropriate repo's software bill-of-materials (e.g. package.json, pom.xml) (-d, --directory)
- Naming a single identifier (-p, --package)

Analysis level is customizable as you can build your own preferred analysis profile in seconds. Dependency Combobulator does come with several analysis levels out-of-the-box, selected by -a, --analysis

Supported output format:
- Screen stdout (default)
- CSV export to designated file -(-CSV)

## Usage examples

https://user-images.githubusercontent.com/90651458/140915800-c267034b-90c9-42d1-b12a-83e12f70d44e.mp4


## Credits

The project is maintained and sponsored by Apiiro with 💜
