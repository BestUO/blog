import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
// import HelloWorld from "../components/HelloWorld.vue";
// import Home from "../views/Home.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        redirect: "/articles"
    },
    // {
    //     path: "*",
    //     redirect: () => {
    //         return {
    //             name: 'message'
    //         }
    //     },
    // },
    // {
    //     path: "/",
    //     name: "Home",
    //     component: import(/* webpackChunkName: "articles" */ "../views/Articles.vue"),
    // },
    // {
    //     path: "/helloWorld",
    //     name: "HelloWorld",
    //     component: HelloWorld,
    // },
    {
      path: "/articles",
      name: "articles",
      // route level code-splitting
      // this generates a separate chunk (articles.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "articles" */ "../views/Articles.vue")
    },
    // {
    //   path: "/archive",
    //   name: "archive",
    //   component: () =>
    //     import(/* webpackChunkName: "archive" */ "../views/Archive.vue")
    // },
    // {
    //   path: "/timeline",
    //   name: "timeline",
    //   component: () =>
    //     import(/* webpackChunkName: "timeline" */ "../views/Timeline.vue")
    // },
    // {
    //   path: "/project",
    //   name: "project",
    //   component: () =>
    //     import(/* webpackChunkName: "project" */ "../views/Project.vue")
    // },
    // {
    //   path: "/message",
    //   name: "message",
    //   component: () =>
    //     import(/* webpackChunkName: "message" */ "../views/Message.vue")
    // },
    {
      path: "/about",
      name: "about",
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/About.vue")
    },
    {
      path: "/articleDetail",
      name: "articleDetail",
      component: () =>
        import(/* webpackChunkName: "articleDetail" */ "../views/ArticleDetail.vue")
    },
    {
        path: '/404',
        name: "404",
        component: () => 
        import('../views/404.vue')
    },
    {
        path: '/:pathMatch(.*)',
        redirect: '/404'
    }
];

const router = createRouter({
    // history: createWebHistory(process.env.BASE_URL),
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
