import { unset } from 'lodash-es';

export function changeAttribute(attributes, event, attribute, value) {
  if (event.entering) {
    attributes[attribute] = value
  } else {
    attributes = unset(attributes, attribute)
  }
  return attributes
}

export function applyAttribute(node, event, attributes, attribute) {
  if (typeof attribute == 'string') {
    changeAttribute(attributes, event, attribute, true)
  } else if (typeof attribute == 'function') {
    attribute(node, event, attributes)
  }
}
