const fs = require('fs')
const path = require('path')

const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')


module.exports = (env, argv) => {

    const devMode = argv.mode === 'development'

    fs.open('./src/config/env.js', 'w', function(err, fd) {
        let buf = 'export default "development";'
        if (!devMode) {
            buf = 'export default "production";'
        }
        fs.write(fd, buf, 0, buf.length, function(err, written, buffer) {})
    })

    return {
        entry: {
            main: path.resolve(__dirname, './src/main.js'),
            vendors: path.resolve(__dirname, './src/vendors.js')
        },

        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: devMode ? '[name].js' : '[name].[chunkhash].js',
            chunkFilename: '[id].[chunkhash].js',
            //publicPath: devMode ? '/assets/' : publicPath
        },

        module: {
            rules: [
                {
                    test: /\.vue$/,
                    use: [{
                            loader: 'vue-loader'
                        }
                    ],
                    exclude: /node_modules/
                }, 
                { 
                    test: /\.js$/, 
                    use: [
                        {
                            loader: 'babel-loader',
                        }
                    ],
                    exclude: /node_modules/
                },
                { 
                    test: /\.css$/, 
                    use: [ 
                            devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
                            'css-loader'
                        ] 
                },
                { 
                    test: /\.(styl)|(stylus)$/, 
                    use: [
                            devMode ? 'style-loader' : MiniCssExtractPlugin.loader, 
                            'css-loader', 'stylus-loader'
                        ] 
                },
                {
                    test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
                    use: [{
                            loader: 'url-loader',
                            options: {
                                limit: 10000
                            } 
                        }
                    ]
                }
            ]
        },

        plugins:  [
            new VueLoaderPlugin(),

            new HtmlWebpackPlugin({
                filename: 'index.html',
                chunks: ['main', 'vendors'],
                template: path.resolve(__dirname, './src/assets/templates/index.html')
            })
        ],

        devServer: {
            proxy: {
            }
        },

        devtool: devMode ? '#eval-source-map' : '#source-map',

        resolve: {
            extensions: ['.js', '.vue'],
            alias: {
                '~': path.resolve(__dirname, './src'),
                '@libs': path.resolve(__dirname, './src/libs'),
                '@@config': path.resolve(__dirname, './src/config/config'),
                // '@components': path.resolve(__dirname, './src/components'),
                // '@assets': path.resolve(__dirname, './src/assets'),
                // '@plugins': path.resolve(__dirname, './src/plugins'),
                // '@@config': path.resolve(__dirname, './src/config/config.js'),
                // '@@env': path.resolve(__dirname, './src/config/env.js')
            },
        }
    }
}