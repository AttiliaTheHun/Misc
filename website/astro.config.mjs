// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default {
  site: 'https://elephantslife.eu',
  integrations: [mdx(), sitemap()],
  adapter: cloudflare(),
  output: 'static'
};