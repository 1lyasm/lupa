package main

import (
	"bytes"
	"html/template"
	"log"
	"net/http"
	"os"
    "strconv"
)

type TemplateData struct {
    Count string
}

type Server struct {
    count uint64
}

func (server *Server) generateData() TemplateData {
    return TemplateData{Count: strconv.FormatUint(server.count, 10)}
}

func (server *Server) fillHTML() {
    template, err := template.New("index.tmpl").ParseFiles("index.tmpl")
    if err != nil {
        log.Fatalf("fillHTML: ParseFiles failed: %e", err)
    }
    template_data := server.generateData()
    var buffer bytes.Buffer
    err = template.Execute(&buffer, template_data)
    if err != nil {
        log.Fatalf("fillHtml: Execute failed: %e", err)
    }
    err = os.WriteFile("index.html", buffer.Bytes(), 0644)
    if err != nil {
        log.Fatalf("fillHTML: WriteFile failed: %e", err)
    }
}

func (server *Server) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    path := req.URL.Path
    if path == "/increment" {
        server.count += 1
    }
    server.fillHTML();
    http.ServeFile(w, req, "index.html")
}


func main() {
    handler := &Server{count: 0}
	http.Handle("/", handler)
	http.Handle("/increment", handler)
	http.ListenAndServe(":6789", nil)
}

