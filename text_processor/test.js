const fs = require('fs');
const markdownit = require('markdown-it')

// docs:https://github.com/markdown-it/markdown-it

md = new markdownit()
fs.readFile('./test.md','utf-8',(error,data)=>{
    if(error){
        console.log("Error:",error);
        return;
    }
    const a = md.render(data);
    console.log(a)
})
