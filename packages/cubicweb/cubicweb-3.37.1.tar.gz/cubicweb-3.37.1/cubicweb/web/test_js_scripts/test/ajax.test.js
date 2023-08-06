const fs = require("fs");

function loadUrl(url) {
  return fs.readFileSync(url, "utf8");
}

function fakeXHRRequest(deferred) {
  const xhr = { readyState: 0 };
  deferred._req = xhr;

  function success(value) {
    xhr.readyState = 4;
    deferred.success(value);
  }

  function error(status, err) {
    xhr.readyState = 4;
    deferred.error(xhr, status, err);
  }

  return { success, error };
}

describe("ajax", () => {
  let root;
  beforeEach(() => {
    document.body.innerHTML = "";
    document.head.innerHTML = "";
    root = document.createElement("div");
    root.id = "fixture";
    document.body.appendChild(root);
    // re-initialize cw loaded cache so that each tests run in a
    // clean environment, have a lookt at _loadAjaxHtmlHead implementation
    // in cubicweb.ajax.js for more information.
    cw.loaded_scripts = [];
    cw.loaded_links = [];

    jest.spyOn(window, "loadRemote").mockImplementation((url) => {
      const d = new Deferred();
      const { success, error } = fakeXHRRequest(d);
      try {
        const content = loadUrl(url);
        success(content);
      } catch {
        error(404, "File not found");
      }
      return d;
    });
  });

  function jsSources() {
    return $.map($("head script[src]"), function (script) {
      return script.getAttribute("src");
    });
  }

  test("test simple h1 inclusion (ajax_url0.html)", (done) => {
    expect($("#fixture").children().length).toBe(0);
    $("#fixture")
      .loadxhtml("data/ajax_url0.html", null, "GET")
      .addCallback(function () {
        try {
          expect($("#fixture").children().length).toBe(1);
          expect($("#fixture h1").html()).toBe("Hello");
        } finally {
          done();
        }
      });
  });

  test("test simple html head inclusion (ajax_url1.html)", (done) => {
    var scriptsIncluded = jsSources();
    expect(jQuery.inArray("http://foo.js", scriptsIncluded)).toBe(-1);
    $("#fixture")
      .loadxhtml("data/ajax_url1.html", null, "GET")
      .addCallback(function () {
        try {
          var origLength = scriptsIncluded.length;
          scriptsIncluded = jsSources();
          // check that foo.js has been prepended to <head>
          expect(scriptsIncluded.length).toBe(origLength + 1);
          expect(scriptsIncluded.indexOf("http://foo.js")).toBe(0);
          // check that <div class="ajaxHtmlHead"> has been removed
          expect($("#fixture").children().length).toBe(1);
          expect($("div.ajaxHtmlHead").length).toBe(0);
          expect($("#fixture h1").html()).toBe("Hello");
        } finally {
          done();
        }
      });
  });

  test("test addCallback", (done) => {
    expect($("#fixture").children().length).toBe(0);
    var d = $("#fixture").loadxhtml("data/ajax_url0.html", null, "GET");
    d.addCallback(function () {
      try {
        expect($("#fixture").children().length).toBe(1);
        expect($("#fixture h1").html()).toBe("Hello");
      } finally {
        done();
      }
    });
  });

  test("test callback after synchronous request", () => {
    var deferred = new Deferred();

    deferred._req = { readyState: 4 };
    deferred.success(1);

    let switchedSync = false;
    deferred.addCallback(function () {
      switchedSync = true;
    });
    expect(switchedSync).toBe(true);
  });

  test("test addCallback with parameters", (done) => {
    expect($("#fixture").children().length).toBe(0);
    var d = $("#fixture").loadxhtml("data/ajax_url0.html", null, "GET");
    d.addCallback(
      function (_data, _req, arg1, arg2) {
        try {
          expect(arg1).toBe("Hello");
          expect(arg2).toBe("world");
        } finally {
          done();
        }
      },
      "Hello",
      "world"
    );
  });

  test("test callback after synchronous request with parameters", (done) => {
    var deferred = new Deferred();
    deferred.addCallback(
      function (_data, _req, arg1, arg2) {
        // add an assertion to ensure the callback is executed
        try {
          expect(arg1).toBe("Hello");
          expect(arg2).toBe("world");
        } finally {
          done();
        }
      },
      "Hello",
      "world"
    );
    deferred.addErrback(function () {
      // throw an exception to start errback chain
      try {
        throw this._error;
      } finally {
        done();
      }
    });
    const { success } = fakeXHRRequest(deferred);
    success(loadUrl("data/ajax_url0.html"));
  });

  test("test addErrback", () => {
    var d = $("#fixture").loadxhtml("data/nonexistent.html", null, "GET");
    d.addCallback(function () {
      // should not be executed
      assert.ok(false, "callback is executed");
    });
    const errback = jest.fn();
    d.addErrback(errback);
    expect(errback).toBeCalled();
  });

  test("test callback execution order", () => {
    var counter = 1;
    var d = $("#fixture").loadxhtml("data/ajax_url0.html", null, "GET");
    d.addCallback(function () {
      counter *= 2;
      expect(counter).toBe(2);
    });
    d.addCallback(function () {
      counter *= 3;
      expect(counter).toBe(6);
    });
    d.addCallback(function () {
      counter *= 5;
      expect(counter).toBe(30);
    });
    expect(counter).toBe(30);
  });

  test("test already included resources are ignored (ajax_url1.html)", (done) => {
    var scriptsIncluded = jsSources();
    // NOTE:
    expect(jQuery.inArray("http://foo.js", scriptsIncluded)).toBe(-1);
    /* use endswith because in pytest context we have an absolute path */
    $("#fixture")
      .loadxhtml("data/ajax_url1.html", null, "GET")
      .addCallback(function () {
        var origLength = scriptsIncluded.length;
        scriptsIncluded = jsSources();
        try {
          // check that foo.js has been inserted in <head>
          expect(scriptsIncluded.length).toBe(origLength + 1);
          expect(scriptsIncluded.indexOf("http://foo.js")).toBe(0);
          // check that <div class="ajaxHtmlHead"> has been removed
          expect($("#fixture").children().length).toBe(1);
          expect($("div.ajaxHtmlHead").length).toBe(0);
          expect($("#fixture h1").html()).toBe("Hello");
        } finally {
          done();
        }
      });
  });

  test("test event on CubicWeb", (done) => {
    var events = null;
    $(CubicWeb).bind("server-response", function () {
      // check that server-response event on CubicWeb is triggered
      events = "CubicWeb";
    });
    $("#fixture")
      .loadxhtml("data/ajax_url0.html", null, "GET")
      .addCallback(function () {
        try {
          expect(events).toBe("CubicWeb");
        } finally {
          done();
        }
      });
  });

  test("test event on node", (done) => {
    var nodes = [];
    $("#fixture").bind("server-response", function () {
      nodes.push("node");
    });
    $(CubicWeb).bind("server-response", function () {
      nodes.push("CubicWeb");
    });
    $("#fixture")
      .loadxhtml("data/ajax_url0.html", null, "GET")
      .addCallback(function () {
        try {
          expect(nodes.length).toBe(2);
          // check that server-response event on CubicWeb is triggered
          // only once and event server-response on node is triggered
          expect(nodes[0]).toBe("CubicWeb");
          expect(nodes[1]).toBe("node");
        } finally {
          done();
        }
      });
  });
});
