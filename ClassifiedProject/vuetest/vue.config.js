// const { defineConfig } = require("@vue/cli-service");
// module.exports = defineConfig({
//   transpileDependencies: true,
// });

// vue.config.js 配置

// module.exports = {
//   runtimeCompiler: true,
//   publicPath: "./", // 设置打包文件相对路径
//   outputDir: "dist", // 构建时输出的目录根路径
//   // assetsDir: 'static',  // 放置静态资源的目录
//   // indexPath: 'index.html', // HTML输出的路径
//   devServer: {
//     // proxy: "http://localhost:8000",
//     port: "8080",
//     proxy: {
//       "/api": {
//         // 配置到接口包含api使用该代理
//         target: "http://127.0.0.1:8000/api", // 定义后端的接口
//         changeOrigin: true,
//         ws: true,
//         pathRewrite: {
//           "^/api": "",
//         },
//       },
//     },
//   },
// };

module.exports = {
    devServer: {
        open: true,
        host: 'localhost',
        port: 8080,
        https: false,
        //以上的ip和端口是我们本机的;下面为需要跨域的
        proxy: {//配置跨域
            '/api': {
                target: 'http://localhost:8000/api/',//这里后台的地址模拟的;应该填写你们真实的后台接口
                ws: true,
                changOrigin: true,//允许跨域
                pathRewrite: {
                    '^/api': ''//请求的时候使用这个api就可以
                }
            }
            
        }
    }
}
