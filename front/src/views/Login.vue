<script>

</script>

<template>
    <div class="container">
        <h1>Вход</h1>
        <form id="register">
            <div class="field">
                <input class="input-field" placeholder="Имя">
            </div>
            <div class="field">
                <input class="input-field" placeholder="Фамилия">
            </div>
            <div class="field">
                <input class="input-field" placeholder="Пароль">
            </div>
            <hr>
            <div class="button-field">
                <button id="accept">Войти</button>
            </div>
            <div class="auth-link">
                <p>Нет аккаунт? <a href="Reg.vue">Зарегистрироваться</a></p>
            </div>
        </form>
    </div>
</template>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: white;
    color: #222;
    margin: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.container {
    display: flex;
    max-width: 800px;
    padding: 30px;
    align-items: center;
    flex-direction: column;
    border: solid 2px #777;
    border-radius: 30px;
    text-align: center;
}

h1 {
    color: #222;
    margin-bottom: 20px;
}

.field {
    display: block;
    margin-bottom: 20px;
    width: 400px;
    border: solid 2px #777;
    border-radius: 20px;
    height: 40px;
    text-align: left;
}

input {
    color: #222;
    font-size: 12px;
    border: none;
    margin: 13px 20px;
}

hr {
    width: 90%;
    border: none;
    height: 1px;
    background-color: #777;
    margin: 30px auto;
}

.button-field {
    display: block;
    margin-bottom: 20px;
    width: 400px;
    border: solid 2px #222;
    background-color: #222;
    border-radius: 20px;
    height: 40px;
}

button {
    display: block;
    border: none;
    background-color: #222;
    color: #eee;
    margin: 10px auto;
}

p {
    font-size: 12px;
}

a {
    text-decoration: none;
}
</style>