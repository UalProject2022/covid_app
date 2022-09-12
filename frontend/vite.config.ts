import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { defineConfig } from 'vite'


// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		host: '0.0.0.0',
		port: 5173,
	},
	preview: {
		port: 5173
	},
	build: {
		rollupOptions: {
			input: {
				main: resolve('index.html'),
			}
		}
	}
})
