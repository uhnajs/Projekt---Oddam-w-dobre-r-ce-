
{% load static %}

<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="ie=edge" />
  <title>{% block title %}Formularz oddania darów{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}" />
</head>
<body>
{% block content %}
<header class="header--main-page">
  <nav class="container container--70">
    <!-- User Authentication Links -->
    {% if user.is_authenticated %}
      <ul class="nav--actions">
        <li class="logged-user">
          Witaj {{ user.first_name|default:user.username }}
          <ul class="dropdown">
            <li><a href="#">Profil</a></li>
            <li><a href="#">Ustawienia</a></li>
            <li><a href="{% url 'logout' %}">Wyloguj</a></li>
          </ul>
        </li>
      </ul>
    {% else %}
      <ul class="nav--actions">
        <li><a href="{% url 'login' %}" class="btn btn--small btn--without-border">Zaloguj</a></li>
        <li><a href="{% url 'register' %}" class="btn btn--small btn--highlighted">Załóż konto</a></li>
      </ul>
    {% endif %}
    <!-- Main Navigation -->
    <ul>
      <li><a href="/" class="btn btn--without-border active">Start</a></li>
      <li><a href="/#steps" class="btn btn--without-border">O co chodzi?</a></li>
      <li><a href="/#about-us" class="btn btn--without-border">O nas</a></li>
      <li><a href="/#help" class="btn btn--without-border">Fundacje i organizacje</a></li>
      <li><a href="{% url 'form' %}" class="btn btn--without-border">Przekaż dary</a></li>
      <li><a href="/#contact" class="btn btn--without-border">Kontakt</a></li>
    </ul>
  </nav>
  <!-- Header Slogan -->
  <div class="slogan container container--90">
    <div class="slogan--item">
      <h1>Oddaj rzeczy, których już nie chcesz<br /><span class="uppercase">potrzebującym</span></h1>
      <div class="slogan--steps">
        <div class="slogan--steps-title">Wystarczą 4 proste kroki:</div>
        <ul class="slogan--steps-boxes">
          <li><div><em>1</em><span>Wybierz rzeczy</span></div></li>
          <li><div><em>2</em><span>Spakuj je w worki</span></div></li>
          <li><div><em>3</em><span>Wybierz fundację</span></div></li>
          <li><div><em>4</em><span>Zamów kuriera</span></div></li>
        </ul>
      </div>
    </div>
  </div>
</header>



<!-- Footer -->
<footer>
  <div class="contact">
    <h2>Skontaktuj się z nami</h2>
    <h3>Formularz kontaktowy</h3>
    <form class="form--contact">
      <div class="form-group form-group--50">
        <input type="text" name="name" placeholder="Imię" />
      </div>
      <div class="form-group form-group--50">
        <input type="text" name="surname" placeholder="Nazwisko" />
      </div>
      <div class="form-group">
        <textarea name="message" placeholder="Wiadomość" rows="1"></textarea>
      </div>
      <button class="btn" type="submit">Wyślij</button>
    </form>
  </div>
  <div class="bottom-line">
    <span class="bottom-line--copy">Copyright &copy; 2018</span>
    <div class="bottom-line--icons">
      <a href="#" class="btn btn--small"><img src="{% static 'images/icon-facebook.svg' %}" /></a>
      <a href="#" class="btn btn--small"><img src="{% static 'images/icon-instagram.svg' %}" /></a>
    </div>
  </div>
</footer>
{% endblock content %}

{% block extra_js %}
<script src="{% static 'js/app.js' %}"></script>
{% endblock %}
</body>
</html>
