<template>
    <div>
      <nav>
        <router-link to="/">Домашняя</router-link> |
        <router-link to="/login">Логин</router-link> |
        <router-link to="/register">Регистрация</router-link> |
        <router-link to="/admin">Админка</router-link>
      </nav>
      <router-view></router-view>
    </div>
  </template>