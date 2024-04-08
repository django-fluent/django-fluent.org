"use strict";

const path = require("path");
const glob = require('glob');

// Webpack plugins
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const RemoveEmptyScriptsPlugin = require('webpack-remove-empty-scripts');
const LiveReloadPlugin = require('webpack-livereload-plugin');
const WebpackBuildNotifierPlugin = require('webpack-build-notifier');

// PostCSS plugins
const autoprefixer = require("autoprefixer");
const removeSelectors = require("postcss-remove-selectors");
const sortMediaQueries = require("postcss-sort-media-queries");

const paths = {
  root: "./frontend/static",
  dist: "./frontend/static/frontend/dist",
  sass: "./frontend/sass",
  fonts: "./frontend/static/frontend/fonts",
  images: "./frontend/static/frontend/images",
  js: "./frontend/static/frontend/js",
};

let postcss_plugins = [
  // All post-processing happens in one batch, no reparsing of CSS is done here.
  removeSelectors({
    selectors: [
      ".accordion",
      ".btn-outline",
      ".custom-control-input",
      ".custom-file-input",
      ".custom-select",
      ".invalid-tooltip",
      ".display-1",
      ".display-2",
      ".display-3",
      ".display-4",
      ".form-control-file",
      ".form-control-plaintext",
      ".form-control-sm",
      ".form-control-lg",
      ".form-control.is-valid",
      ".form-check-input.is-valid",
      ".nav-pills",
      ".nav-tabs",
      ".show > .btn",
      ".navbar-dark",
      ".navbar-expand ", // only md
      ".pagination-lg",
      ".pagination-sm",
      ".table .thead-dark",
      ".table .thead-light",
      ".table-active",
      ".table-bordered",
      ".table-borderless",
      ".table-danger",
      ".table-dark",
      ".table-hover",
      ".table-light",
      ".table-info",
      ".table-primary",
      ".table-success",
      ".table-responsive",
      ".table-secondary",
      ".table-striped",
      ".table-warning",
      ".order-",
      ".valid-feedback",
      ".valid-tooltip",
      ".was-validated",
    ]
  }),
  autoprefixer({
    cascade: false
  }),
  sortMediaQueries({sort: 'mobile-first'}), // combine media queries
];

// Pre-build step to generate webp images.
// Otherwise css-loader can't resolve them as URL.
(async () => {
    const imagemin = (await import('imagemin')).default;
    const imageminWebp = (await import('imagemin-webp')).default;
    await imagemin([`${paths.images}/*.{jpg,png}`], {
        destination: paths.images,
        plugins: [
            imageminWebp({quality: 80})
        ]
    });

    console.log('Generated webP images');
})();

// *.js and *.scss as entries
let entries = {};
glob.sync(path.join(__dirname, `${paths.js}/*.js`)).forEach((f) => entries[path.basename(f, '.js')] = f);
glob.sync(path.join(__dirname, `${paths.js}/*.ts`)).forEach((f) => entries[path.basename(f, '.ts')] = f);
glob.sync(path.join(__dirname, `${paths.sass}/*.scss`)).forEach((f) => entries[path.basename(f, '.scss')] = f);

module.exports = {
  target: 'web',
  entry: entries,
  devtool: 'source-map',
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],  // for import statements
    modules: [
      path.join(__dirname, paths.sass),
      path.join(__dirname, paths.root),
      'node_modules'
    ],
  },
  output: {
    publicPath: "/static/frontend/",
    path: path.join(__dirname, paths.dist),
    filename: '[name].min.js', // Forces webpack to multiple output files
    assetModuleFilename: '[name][ext]',  // '[name][contenthash][ext]'
    sourceMapFilename: "[file].map",
    clean: true,
  },
  plugins: [
    // Plugins also work for produced assets (in contrast to loaders).
    new MiniCssExtractPlugin({filename: '[name].css'}),
    new RemoveEmptyScriptsPlugin(),
    new LiveReloadPlugin(),
    new WebpackBuildNotifierPlugin({
      title: "Django-Fluent",
      /*logo: path.join(__dirname, "../web/favicon-32x32.png"),*/
      suppressWarning: true,
      suppressSuccess: true,
    })
  ],
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin(),
      new CssMinimizerPlugin(),
    ],
  },
  module: {
    rules: [
      {
        // Generate JavaScript from TypeScript
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        // Generate CSS from imports/entries.
        test: /\.(css|scss)$/,
        //type: "asset/resource",
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: './'
            }
          },
          {
            // Translates CSS to CommonJS tokens
            loader: "css-loader",
            options: {
              sourceMap: true,
              //url: false  // Don't process url(), is manually copied (e.g. for webp images)
            }
          },
          {
            // Apply PostCSS filters
            loader: "postcss-loader",
            options: {
              sourceMap: true,
              postcssOptions: {
                plugins: postcss_plugins,
              }
            }
          },
          {
            // Convert SCSS
            loader: "sass-loader",
            options: {
              sourceMap: true,
              sassOptions: {
                includePaths: [
                  "./frontend/sass-vendor"
                ]
              }
            }
          }
        ]
      },
      {
        // Minifiy images found via url(..)
        test: /\.(jpg|jpeg|png|gif|svg|webp)$/,
        type: "asset/resource",
        use: [
          {
            loader: 'image-webpack-loader',
            options: {
              mozjpeg: {quality: 80, progressive: true},
              pngquant: {speed: 1, strip: true, quality: [0.65, 0.8], verbose: true},
              webp: {quality: 80, method: 6},
              svgo: {plugins: [{name: 'removeViewBox', active: false}]}
            }
          }
        ]
      }
    ]
  },
};
