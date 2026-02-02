module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  lintOnSave: process.env.NODE_ENV !== 'production',
  productionSourceMap: false,
  devServer: {
    port: 8080,
    host: '0.0.0.0',
    https: false,
    open: false,
    hot: true,
    disableHostCheck: true,
    overlay: {
      warnings: false,
      errors: true
    },
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    },
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          libs: {
            name: 'chunk-libs',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          elementUI: {
            name: 'chunk-elementUI',
            priority: 20,
            test: /[\\/]node_modules[\\/]_?element-ui(.*)/
          },
          commons: {
            name: 'chunk-commons',
            test: /[\\/]src[\\/]/,
            minChunks: 3,
            priority: 5,
            reuseExistingChunk: true
          },
          vendors: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: -10,
            chunks: 'all'
          }
        }
      },
      runtimeChunk: 'single'
    },
    performance: {
      hints: process.env.NODE_ENV === 'production' ? 'warning' : false,
      maxAssetSize: 30000000,
      maxEntrypointSize: 50000000
    }
  },
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'Free SSL Service'
      args[0].minify = {
        removeComments: true,
        collapseWhitespace: true,
        removeAttributeQuotes: true
      }
      return args
    })
    
    // Add bundle analyzer
    if (process.env.NODE_ENV === 'production') {
      config.plugin('webpack-bundle-analyzer')
        .use(require('webpack-bundle-analyzer').BundleAnalyzerPlugin)
        .end()
    }
    
    // Optimize images
    config.module
      .rule('images')
      .use('image-webpack-loader')
      .loader('image-webpack-loader')
      .options({
        mozjpeg: {
          progressive: true,
          quality: 65
        },
        optipng: {
          enabled: false
        },
        pngquant: {
          quality: [0.65, 0.90],
          speed: 4
        },
        gifsicle: {
          interlaced: false
        }
      })
      .end()
    
    // Cache optimization
    config.cache({
      type: 'filesystem',
      buildDependencies: {
        config: [__filename]
      }
    })
  },
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    },
    extract: process.env.NODE_ENV === 'production',
    sourceMap: false,
    requireModuleExtension: true
  }
}
