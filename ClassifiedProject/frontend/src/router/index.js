import Vue from "vue";
import VueRouter from "vue-router";
import projectList from "../components/project/projectList.vue";
import Login from "../views/Login.vue";
import Navigation from "../views/Navigation.vue";

Vue.use(VueRouter);
const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/main",
    name: "Navigation",
    component: Navigation,
    children: [
      {
        path: "project",
        component: projectList,
      },
      {
        path: "about",
        name: "About",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
          import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// 导航守卫，控制一些页面登录才能访问
router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    // 当路由为login时就直接下一步操作
    next();
  } else {
    // 否则就需要判断
    if (sessionStorage.session) {
      // 如果有用户名就进行下一步操作
      next();
    } else {
      next({ path: "/login" }); // 没有用户名就跳转到login页面
    }
  }
});

export default router;