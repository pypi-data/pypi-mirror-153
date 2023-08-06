const { datetuple } = require("./utils");

describe("datetime", () => {
  test("test full datetime", () => {
    expect(cw.utils.toISOTimestamp(new Date(1986, 3, 18, 10, 30, 0, 0))).toBe(
      "1986-04-18 10:30:00"
    );
  });

  test("test only date", () => {
    expect(cw.utils.toISOTimestamp(new Date(1986, 3, 18))).toBe(
      "1986-04-18 00:00:00"
    );
  });

  test("test null", () => {
    expect(cw.utils.toISOTimestamp(null)).toBeNull();
  });
});

describe("parsing", () => {
  test("test basic number parsing", () => {
    var d = strptime("2008/08/08", "%Y/%m/%d");
    expect(datetuple(d)).toEqual([2008, 8, 8, 0, 0]);
    d = strptime("2008/8/8", "%Y/%m/%d");
    expect(datetuple(d)).toEqual([2008, 8, 8, 0, 0]);
    d = strptime("8/8/8", "%Y/%m/%d");
    expect(datetuple(d)).toEqual([8, 8, 8, 0, 0]);
    d = strptime("0/8/8", "%Y/%m/%d");
    expect(datetuple(d)).toEqual([0, 8, 8, 0, 0]);
    d = strptime("-10/8/8", "%Y/%m/%d");
    expect(datetuple(d)).toEqual([-10, 8, 8, 0, 0]);
    d = strptime("-35000", "%Y");
    expect(datetuple(d)).toEqual([-35000, 1, 1, 0, 0]);
  });

  test("test custom format parsing", () => {
    var d = strptime("2008-08-08", "%Y-%m-%d");
    expect(datetuple(d)).toEqual([2008, 8, 8, 0, 0]);
    d = strptime("2008 - !  08: 08", "%Y - !  %m: %d");
    expect(datetuple(d)).toEqual([2008, 8, 8, 0, 0]);
    d = strptime("2008-08-08 12:14", "%Y-%m-%d %H:%M");
    expect(datetuple(d)).toEqual([2008, 8, 8, 12, 14]);
    d = strptime("2008-08-08 1:14", "%Y-%m-%d %H:%M");
    expect(datetuple(d)).toEqual([2008, 8, 8, 1, 14]);
    d = strptime("2008-08-08 01:14", "%Y-%m-%d %H:%M");
    expect(datetuple(d)).toEqual([2008, 8, 8, 1, 14]);
  });
});

describe("sliceList", () => {
  test("test slicelist", () => {
    var list = ["a", "b", "c", "d", "e", "f"];
    expect(cw.utils.sliceList(list, 2)).toEqual(["c", "d", "e", "f"]);
    expect(cw.utils.sliceList(list, 2, -2)).toEqual(["c", "d"]);
    expect(cw.utils.sliceList(list, -3)).toEqual(["d", "e", "f"]);
    expect(cw.utils.sliceList(list, 0, -2)).toEqual(["a", "b", "c", "d"]);
    expect(cw.utils.sliceList(list)).toEqual(list);
  });
});

describe("formContents", () => {
  // XXX test fckeditor
  test("test formContents", () => {
    const testForm = document.createElement("form");
    document.body.appendChild(testForm);
    $(testForm).append(
      '<input name="input-text" ' + 'type="text" value="toto" />'
    );
    $(testForm).append(
      '<textarea rows="10" cols="30" ' +
        'name="mytextarea">Hello World!</textarea> '
    );
    $(testForm).append('<input name="choice" type="radio" ' + 'value="yes" />');
    $(testForm).append(
      '<input name="choice" type="radio" ' + 'value="no" checked="checked"/>'
    );
    $(testForm).append(
      '<input name="check" type="checkbox" ' + 'value="yes" />'
    );
    $(testForm).append(
      '<input name="check" type="checkbox" ' + 'value="no" checked="checked"/>'
    );
    $(testForm).append(
      '<select id="theselect" name="theselect" ' +
        'multiple="multiple" size="2"></select>'
    );
    $("#theselect").append(
      '<option selected="selected" ' +
        'value="foo">foo</option>' +
        '<option value="bar">bar</option>'
    );
    //Append an unchecked radio input : should not be in formContents list
    $(testForm).append(
      '<input name="unchecked-choice" type="radio" ' + 'value="one" />'
    );
    $(testForm).append(
      '<input name="unchecked-choice" type="radio" ' + 'value="two"/>'
    );
    expect(cw.utils.formContents($(testForm)[0])).toEqual([
      ["input-text", "mytextarea", "choice", "check", "theselect"],
      ["toto", "Hello World!", "no", "no", "foo"],
    ]);
  });
});
