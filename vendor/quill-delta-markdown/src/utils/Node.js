import { isArray, isString, pull } from 'lodash-es';

var id = 0

class Node {
  constructor(data) {
    this.id = ++id
    if (isArray(data)) {
      this.open = data[0]
      this.close = data[1]
    } else if (isString(data)) {
      this.text = data
    }
    this.children = []
  }

  append(e) {
    if (!(e instanceof Node)) {
      e = new Node(e)
    }
    if (e._parent) {
      pull(e._parent.children, e)
    }
    e._parent = this
    this.children = this.children.concat(e)
  }

  render() {
    var text = ''
    if (this.open) {
      text += this.open
    }
    if (this.text) {
      text += this.text
    }
    for (var i = 0; i < this.children.length; i++) {
      text += this.children[i].render()
    }
    if (this.close) {
      text += this.close
    }
    return text
  }

  parent() {
    return this._parent
  }
}

export default Node
