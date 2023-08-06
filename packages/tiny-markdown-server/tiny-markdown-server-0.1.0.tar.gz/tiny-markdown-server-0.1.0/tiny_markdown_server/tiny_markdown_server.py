from http.server import SimpleHTTPRequestHandler, HTTPServer
import time
import urllib
import os
import markdown
import secrets

hostName = "localhost"
serverPort = 8080

reload_urls = {}

startHTML="""
<html>
  <head>
    <style type='text/css'>
<!--
"""

cssData="""
img {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px;
  width: 750px;
}
"""

cssEnd="""
-->
    </style>
  </head>
  <body>
"""

endHTML="""
  </body>
</html>"""


jsonResponseTrue = '{ "refresh": true }'
jsonResponseFalse = '{ "refresh": false }'


def create_reloader(time_and_path):
    scan_url_path = "/" + secrets.token_urlsafe(16)
    reload_urls[scan_url_path] = time_and_path
    return """
<script>
    function poller() {
        fetch(\"""" + scan_url_path + """\")
            .then(response => { if (response.status === 200) { response.json() } else { location.reload(); } })
            .then(data => { if (data && data["refresh"] === true) location.reload(); });        
 
        setTimeout(poller, 500);
    }

    window.onload = function() {
        setTimeout(poller, 500);
    }
</script>
"""

class MDServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        (base, ext) = os.path.splitext(self.path)
        if ext == '.md':
            md_path = os.path.join(os.getcwd(), self.path[1:])
            with open(md_path) as fp:
                md_data = fp.read()
            html = markdown.markdown(md_data, extensions=['tables'])
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(startHTML, "utf-8"))
            self.wfile.write(bytes(cssData, "utf-8"))
            self.wfile.write(bytes(cssEnd, "utf-8"))
            self.wfile.write(bytes(html, "utf-8"))
            reload_data = create_reloader((md_path, os.path.getmtime(md_path)))
            self.wfile.write(bytes(reload_data, "utf-8"))
            self.wfile.write(bytes(endHTML, "utf-8"))
        elif self.path in reload_urls.keys():
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            scan_path_data = reload_urls[self.path]
            if os.path.getmtime(scan_path_data[0]) > scan_path_data[1]:
                self.wfile.write(bytes(jsonResponseTrue, "utf-8"))
                del reload_urls[self.path]
            else:
                self.wfile.write(bytes(jsonResponseFalse, "utf-8"))
        else:
            SimpleHTTPRequestHandler.do_GET(self)

def main(args=None):
    webServer = HTTPServer((hostName, serverPort), MDServer)
    print("Markdown Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")  


if __name__ == "__main__":        
    main()