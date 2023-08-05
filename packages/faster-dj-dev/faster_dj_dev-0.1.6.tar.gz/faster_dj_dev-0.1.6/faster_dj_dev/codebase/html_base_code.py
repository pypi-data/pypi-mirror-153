
pure_base_html_boilerlate = """\n
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
    	<title>Django</title>
	</head>

	<body>
        {% block content %} {% endblock  %}
	</body>
</html>
"""

pure_home_html_boilerlate = """\n
{% extends 'base.html' %}

{% block content %} 
    <style>
        h1{
            display:flex; 
            justify-content:center; 
            align-items:center; 
            width: 100vw;
            height:100vh;
        }
    </style>
        <h1>
            Django is working ...
        </h1> 
    
{% endblock %}
"""


django_htmx_base_html = """\n
{% load django_htmx %}
{% load static %}
<!DOCTYPE html>
<html lang="en">
	<head>
    <title>Django HTMX</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
        <script src="https://unpkg.com/htmx.org@1.7.0" integrity="sha384-EzBXYPt0/T6gxNp0nuPtLkmRpmDBbjg6WmCUZRLXBBwYYmwAUxzlSGej0ARHX0Bo" crossorigin="anonymous" defer></script>
		{% django_htmx_script %}
	</head>

	<body>
        <!--CODE HERE-->
	</body>
</html>
"""

django_tailwind_base_html = """\n
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
	<head>
    <title>Django Tailwind</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
		{% tailwind_css %}
	</head>

	<body>
        <!--CODE HERE-->
	</body>
</html>
"""

django_tailwind_base_html_boilerplate = """\n
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
    	<title>Django Tailwind</title>
		{% tailwind_css %}
	</head>

	<body>
       {% block content %} {% endblock  %}
	</body>
</html>
"""

django_tailwind_home_html_boilerplate = """\n
{% extends 'base.html' %}
{% block content %}
	<h1 class="w-screen h-screen flex items-center justify-center">Django is working ...</h1>
 {% endblock  %}

"""

django_unicorn_base_html = """\n
{ % load unicorn % }
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Unicorn</title>
    { % unicorn_scripts % }
</head>
<body>
    { % csrf_token % }
    <!--CODE HERE-->
</body>
</html>
"""