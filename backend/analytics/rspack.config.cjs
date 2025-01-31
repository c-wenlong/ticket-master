// @ts-check

const path = require("path");
const { EnvironmentPlugin, CopyRspackPlugin } = require("@rspack/core");

/** @type {import('@rspack/cli').Configuration} */
const config = {
  entry: {
    index: "./src/main.ts",
  },
  target: "node20",
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "dist"),
    libraryTarget: "commonjs2",
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
    extensions: [".ts", ".js"],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  plugins: [
    // Define compile time NODE_ENV for tree shaking
    new EnvironmentPlugin({
      NODE_ENV: process.env.NODE_ENV,
    }),
    new CopyRspackPlugin({
      patterns: [
        {
          from:  path.resolve(__dirname, "global-bundle.pem"),
        },
      ],
    }),
  ],
};
module.exports = config;
