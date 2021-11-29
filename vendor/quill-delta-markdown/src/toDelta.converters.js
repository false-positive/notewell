import isEmpty from 'lodash-es/isEmpty';
import { changeAttribute } from './utils/DOM';

function addOnEnter(name) {
  return (event, attributes) => {
    if (!event.entering) {
      return null
    }
    return {
      insert: event.node.literal,
      attributes: Object.assign({}, attributes, { [name]: true }),
    }
  }
}

const converters = [
  // inline
  { filter: 'code', makeDelta: addOnEnter('code') },
  { filter: 'html_inline', makeDelta: addOnEnter('html_inline') },
  // TODO: underline
  // TODO: strike
  { filter: 'emph', attribute: 'italic' },
  { filter: 'strong', attribute: 'bold' },
  // TODO: script
  {
    filter: 'link',
    attribute: (node, event, attributes) => {
      changeAttribute(attributes, event, 'link', node.destination)
    },
  },
  {
    filter: 'text',
    makeDelta: (event, attributes) => {
      if (isEmpty(attributes)) {
        return { insert: event.node.literal }
      } else {
        return {
          insert: event.node.literal,
          attributes: Object.assign({}, attributes),
        }
      }
    },
  },
  {
    filter: 'softbreak',
    makeDelta: (event, attributes) => {
      if (isEmpty(attributes)) {
        return { insert: ' ' }
      } else {
        return { insert: ' ', attributes: Object.assign({}, attributes) }
      }
    },
  },

  // block
  { filter: 'block_quote', lineAttribute: true, attribute: 'blockquote' },
  {
    filter: 'code_block',
    lineAttribute: true,
    makeDelta: addOnEnter('code-block'),
  },
  {
    filter: 'heading',
    lineAttribute: true,
    makeDelta: (event, attributes) => {
      if (event.entering) {
        return null
      }
      return {
        insert: '\n',
        attributes: Object.assign({}, attributes, { header: event.node.level }),
      }
    },
  },
  {
    filter: 'list',
    lineAttribute: true,
    attribute: (node, event, attributes) => {
      changeAttribute(attributes, event, 'list', node.listType)
    },
  },
  {
    filter: 'paragraph',
    lineAttribute: true,
    makeDelta: (event, attributes) => {
      if (event.entering) {
        return null
      }

      if (isEmpty(attributes)) {
        return { insert: '\n' }
      } else {
        return { insert: '\n', attributes: Object.assign({}, attributes) }
      }
    },
  },

  // embeds
  {
    filter: 'image',
    attribute: (node, event, attributes) => {
      changeAttribute(attributes, event, 'image', node.destination)
      if (node.title) {
        changeAttribute(attributes, event, 'title', node.title)
      }
    },
  },
]

export default converters;
