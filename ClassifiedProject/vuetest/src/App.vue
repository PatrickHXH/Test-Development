<template>
  <div id="app">
    <!-- <nav> -->
    <!-- <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> -->
    <!-- </nav> -->
    <router-view></router-view>
  </div>
</template>

<style>
body {
  margin: 0px 0px 0px;
  display: block;
}
html,
body {
  height: 100%;
  padding: 0;
  margin: 0;
}
* {
  margin: 0;
  padding: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
#nav {
  height: 100%;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
