

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
make_script("https://gradio.s3-us-west-2.amazonaws.com/3.0.11/assets/index.51f4f223.js");
make_style("https://gradio.s3-us-west-2.amazonaws.com/3.0.11/assets/index.cbea297d.css");
