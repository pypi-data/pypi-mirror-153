import { babel } from '@rollup/plugin-babel';
import { nodeResolve } from '@rollup/plugin-node-resolve';
import { terser } from 'rollup-plugin-terser';

const STATIC_DIR = 'wagtail_webradio/static/wagtail_webradio';

const config = [
  {
    input: 'wagtail_webradio/static_src/player/js/main.js',
    output: {
      file: `${STATIC_DIR}/player/js/main.js`,
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      nodeResolve(),
      terser({ mangle: true }),
      babel({ babelHelpers: 'bundled' }),
    ],
  },
];

// Admin

[
  'podcast-chooser.js',
  'podcast-chooser-modal.js',
  'podcast-chooser-telepath.js',
  'podcast-form.js',
].forEach((filename) => {
  config.push({
    input: `wagtail_webradio/static_src/admin/js/${filename}`,
    output: {
      dir: `${STATIC_DIR}/admin/js`,
      format: 'iife',
      sourcemap: true,
      globals: {
        jquery: '$',
      },
    },
    external: ['jquery'],
    plugins: [
      nodeResolve(),
      terser({ mangle: true }),
      babel({ babelHelpers: 'bundled' }),
    ],
  });
});

export default config;
