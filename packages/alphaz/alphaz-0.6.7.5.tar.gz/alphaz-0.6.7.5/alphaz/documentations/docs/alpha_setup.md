# Alpha system 

## OS configuration

!!! important 
    make sure that **Git** is well configured.

### Python

- Python 3.10.4 is required.
[Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) could be used.

There is no constraint but the usual structure is to have:

- a user per configuration (_mes_, _mesacc_, _mesint_ and _mesdev_ for exemple)
- three location per user:
    - *_/home/USER/APP_NAME_* for sources
    - *_/home/USER/configs_* for configurations
    - *_/application/USER/APP_NAME_* for tmp files and logs

!!! note
    This is configured within the conf.json file and could be modified

## Setup

If you just want to use the system go for the **classic** way and if you want to modify it use the **sources** integration.

### Classic

The default installation procedure is:

```sh
pip install alphaz
```

It will install all the **dependencies** automatically.

### Using sources

If you want to edit the sources you could use this procedure to clone the sources and configure it as a **sub module**

1. Clone **alphaz** from the repository _https://github.com/ZAurele/alphaz.git_

    ```sh
    cd <your_project_repository>
    git clone https://github.com/ZAurele/alphaz.git
    ```

2. Launch the setup, it will install all the dependencies and other magical actions.

    ```sh
    python setup.py
    ```

3. Define it as a submodule in your project

## Dependencies

Main dependencies are automatically installed, however if you need specific ones, you will have to install them manually

### Oracle

Oracle client 

## Configuration

### Angular

```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@services/*": ["app/services/*", "src/app/services/*"],
      "@views/*": ["app/views/*", "src/app/views/*"],
      "@models/*": ["app/models/*", "src/app/models/*"],
      "@components/*": ["app/components/*", "src/app/components/*"],
      "@alphaa/*": ["alphaa/*", "src/alphaa/*"],
      "@layout/*": ["app/layout/*", "src/app/layout/*"],
      "@envs/*": ["environments/*", "src/environments/*"],
      "@constants/*": ["app/constants/*", "src/app/constants/*"]
    }
  }
}
```