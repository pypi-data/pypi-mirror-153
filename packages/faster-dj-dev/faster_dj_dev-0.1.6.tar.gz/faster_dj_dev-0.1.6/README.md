
**Faster Django Development**

A Simple tool that makes your Django development faster. It allows you to do the tedious Django tasks quickly. You can use it to create an entire Django project in less than 10 seconds plus options to install the popular Django tools in no time.

**Installation**
### virtual environment is required!

```
python -m virtualenv venv
source venv/bin/activate
pip install faster_dj_dev
```

*To install virtualenv*

```
python -m pip install virtualenv
```

***Example***

Let's use this tool to create a new Django project with all its configurations related to static, media and templates. Also, we will create a new Django app with it.

```
faster_dj_dev --init --working-directory path_of_the_folder --project-folder name_of_the_django_project_folder
faster_dj_dev --create_project --config-templates --config-static --config-media --initial-migrate --app main --run-server
```


***Features***

- Create Django project/app in 10 seconds

- Configuring static files (settings)

- Create starter templates for different projects (HTMX, Tailwind, etc...)

- Configuring media files (settings, urls)

- Configuring templates (settings)

- Install and configure Django packages (quick)

- More ...

***Documentation***

Please check [Doc](https://blog.selmi.tech/blog/post/faster_dj_dev-documentation-how-to-become-a-faster-django-developer335421)