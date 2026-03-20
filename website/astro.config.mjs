// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default {
  site: 'https://elephantslife.eu',
  integrations: [mdx(), sitemap()],
  output: 'static'
};