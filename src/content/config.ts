import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.string(),
    description: z.string(),
    readTime: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { blog }; 