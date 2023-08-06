beforeEach(() => {
  document.body.innerHTML = "";
});
describe("firstSelected", () => {
  let select;
  beforeEach(() => {
    select = document.createElement("select");
    select.multiple = "multiple";
    select.size = 2;
    document.body.appendChild(select);
  });

  test("test first selected", () => {
    $(select).append(
      '<option value="foo">foo</option>' +
        '<option selected="selected" value="bar">bar</option>' +
        '<option value="baz">baz</option>' +
        '<option selected="selecetd"value="spam">spam</option>'
    );
    const selected = firstSelected(select);
    expect(selected.value).toBe("bar");
  });

  test("test first selected 2", () => {
    $(select).append(
      '<option value="foo">foo</option>' +
        '<option value="bar">bar</option>' +
        '<option value="baz">baz</option>' +
        '<option value="spam">spam</option>'
    );
    const selected = firstSelected(select);
    expect(selected).toBeNull();
  });
});

describe("visibilty", () => {
  test("toggleVisibility", () => {
    const div = document.createElement("div");
    document.body.appendChild(div);
    div.id = "foo";
    toggleVisibility("foo");
    expect($("#foo").hasClass("hidden")).toBe(true);
  });
});
