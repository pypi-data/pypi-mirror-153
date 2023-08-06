

function make_style(href) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    document.head.appendChild(link);
}

function make_script(src) {
    const script = document.createElement('script');
    script.type = 'module';
    script.setAttribute("crossorigin", "");
    script.src = src;
    document.head.appendChild(script);
}
make_script("https://gradio.s3-us-west-2.amazonaws.com/3.0.9b10/assets/index.32048461.js");
make_style("https://gradio.s3-us-west-2.amazonaws.com/3.0.9b10/assets/index.9ef0c275.css");
