# What is this?
This is a command line interface (CLI) that is an automated end-to-end client for the JDX API.

It is useful for doing automated testing.

# How to install
1. Install `pipenv` by following these [instructions](https://docs.pipenv.org/en/latest/install/#installing-pipenv).

2. Install the required libraries using pipenv,

    ```bash
    pipenv install --skip-lock
    ```

    If that fails try,

    ```bash
    sudo pipenv install
    ```

# How to use
To run the program you will need to execute python through pipenv.

You can do this one of two ways,
1. Open a pipenv shell and execute the program from within
    ```bash
    pipenv shell
    python client.py
    ```

2. Execute pipenv from outside of a shell (Preferred method)
    ```bash
    pipenv run python client.py
    ```

This end-to-end client is a command line utility so you can provide optional arguments to change its behaviour.

Please use,

```bash
pipenv run python client.py -h
```

to learn more about the optional arguments.

# Example usages

Run every file within the `/files` directory against production server,
```bash
pipenv run python client.py
```

Run all of the files but loop forever (please try not to use this, we are not rate limiting currently),
```bash
pipenv run python client.py -l
```

Submit a single file through the JDX workflow,
```bash
pipenv run python client.py -d replace-with-your-file.txt
```

Choose a different directory of files to submit,
```bash
pipenv run python client.py -d ~/path/to/your/directory/
```

Choose a specific competency framework for the workflow,
```bash
pipenv run python client.py -f c9ac8b62-b659-40d1-a191-0600e92c8b7d
```

Submit a specific file, choose a specific framework, and loop forever,
```bash
pipenv run python client.py -d ./files/replace-with-your-file.txt -f c9ac8b62-b659-40d1-a191-0600e92c8b7d -l
```
