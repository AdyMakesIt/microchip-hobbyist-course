const sharp = require("sharp");
const [, , inp, out, w] = process.argv;
sharp(inp, { density: 144 }).resize({ width: parseInt(w || '1600'), withoutEnlargement: false }).png().toFile(out).then(() => console.log('ok')).catch(e => { console.error(e.message); process.exit(1) });
