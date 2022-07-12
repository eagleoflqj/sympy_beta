<script setup>
import { ref, onMounted, watchEffect } from 'vue'
import { NCard, NA, NScrollbar } from 'naive-ui'
import { MathfieldElement } from 'mathlive'

const props = defineProps({
  input: {
    type: String,
    required: true
  },
  inputCallback: {
    type: Function,
    required: true
  },
  enterCallback: {
    type: Function,
    required: true
  }
})

// use it if subexpressions aren't automatically separate, eg: \frac{1}{2}
// use #0 otherwise, eg: Gamma(x)
const ph = '{#0}'
const small = { class: 'small' }

const parenthesisKey = {
  latex: '\\left(#0\\right)',
  variants: ['(', ')', ',', ph],
  ...small
}
const shiftKey = {
  class: 'action font-glyph modifier',
  label: "<svg><use xlink:href='#svg-shift' /></svg>",
  command: ['performWithFeedback']
}
const leftKey = {
  class: 'action',
  label: "<svg><use xlink:href='#svg-arrow-left' /></svg>",
  command: ['performWithFeedback', 'moveToPreviousChar']
}
const rightKey = {
  class: 'action',
  label: "<svg><use xlink:href='#svg-arrow-right' /></svg>",
  command: ['performWithFeedback', 'moveToNextChar']
}
const backspaceKey = {
  class: 'action font-glyph',
  label: '&#x232b;',
  command: ['performWithFeedback', 'deleteBackward']
}

function capitalize (s) {
  return s[0].toUpperCase() + s.slice(1)
}

function addSpecialKeys (rows, upper, name) {
  const shiftKeyCopy = { ...shiftKey, layer: upper ? `beta-lower-${name}` : `beta-upper-${name}` }
  rows[2].splice(0, 0, shiftKeyCopy)
  rows[2].push(leftKey, rightKey)
  rows[name === 'english' ? 1 : 2].push(backspaceKey)
  return { rows }
}

function betaEnglish (upper) {
  const letterLayout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
  ]
  const rows = letterLayout.map(letters => letters.map(letter => ({
    latex: upper ? letter.toUpperCase() : letter,
    variants: [upper ? letter : letter.toUpperCase()]
  })))
  return addSpecialKeys(rows, upper, 'english')
}

function betaGreek (upper) {
  const letterLayout = [
    ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa'],
    ['lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau'],
    ['upsilon', 'phi', 'chi', 'psi', 'omega']
  ]
  const rows = letterLayout.map(letters => letters.map(letter => ({
    latex: '\\' + (upper ? capitalize(letter) : letter),
    variants: ['\\' + (upper ? letter : capitalize(letter))]
  })))
  return addSpecialKeys(rows, upper, 'greek')
}

function key (latex) {
  return { latex }
}

function trigKey (name) {
  const trig = '\\' + name
  const variants = [{ latex: trig + '^' + ph, insert: trig + '^' + ph + ph, ...small }]
  if (name === 'sin' || name === 'cos' || name === 'tan') {
    const arc = '\\arc' + name
    variants.push({ latex: arc, insert: arc + ph, ...small })
  }
  const result = {
    latex: trig,
    insert: trig + ph,
    variants
  }
  if (name.length > 3) {
    result.class = 'small'
  }
  return result
}

const mulKey = { latex: '*', variants: ['\\cdot', '\\times'] }
const divKey = { latex: '/', variants: ['\\div'] }
const fracKey = { latex: '\\frac' + ph + ph, ...small }
const powKey = { label: '^', insert: '#@^' + ph } // can't use ^{#0} for continuous press
const equalKey = { latex: '=', variants: ['>', '\\geq', '<', '\\leq', '\\neq'] }
const sqrtKey = {
  latex: '\\sqrt' + ph,
  variants: [
    { latex: '\\sqrt[3]' + ph, ...small }, { latex: '\\sqrt[#0]' + ph, ...small }
  ],
  ...small
}
const limKey = { latex: '\\lim', insert: '\\lim_' + ph + ph }
const dirKey = { latex: 'x_0^+', insert: '^+', variants: [{ latex: 'x_0^-', insert: '^-' }] }
const expKey = { latex: '\\exp', insert: '\\exp' + ph }
const lnKey = {
  latex: '\\ln',
  insert: '\\ln' + ph,
  variants: [
    { latex: '\\ln^' + ph, insert: '\\ln^' + ph + ph, ...small },
    { latex: '\\log_' + ph, insert: '\\log_' + ph + ph, ...small },
    { latex: '\\log^' + ph + '_' + ph, insert: '\\log^' + ph + '_' + ph + ph, ...small }
  ]
}
const derivKey = {
  latex: '\\mathrm{d}',
  insert: 'd',
  variants: [
    { latex: '\\frac{\\mathrm{d}' + ph + '}{\\mathrm{d' + ph + '}', insert: '\\frac{d#0}{d#0}', ...small },
    { latex: '\\frac{\\partial' + ph + '}{\\partial' + ph + '}', ...small }]
}
const intKey = {
  latex: '\\int',
  variants: [{ latex: '\\int_0^\\infty', ...small },
    { latex: '\\int_{-\\infty}^\\infty', ...small },
    { latex: '\\int_' + ph + '^' + ph, ...small }],
  ...small
}
const gammaKey = { latex: '\\Gamma', insert: '\\Gamma\\left(#0\\right)' }
const betaKey = { latex: '\\Beta', insert: '\\Beta\\left(#0, #0\\right)' }
const xKey = { latex: 'x', variants: ['y', 'z', 'f'] }

const betaKeyboardLayer = {
  'beta-basic': {
    rows: [
      [key('7'), key('8'), key('9'), key('+'), key('-'), mulKey, key('e'), equalKey, parenthesisKey],
      [key('4'), key('5'), key('6'), divKey, fracKey, powKey, key('i'), key('!'), backspaceKey],
      [key('1'), key('2'), key('3'), key('0'), key('.'), sqrtKey, key('\\pi'), leftKey, rightKey]
    ]
  },
  'beta-math': {
    rows: [
      [trigKey('sin'), trigKey('cos'), trigKey('tan'), limKey, key('\\to'), dirKey, key('\\infty'), parenthesisKey],
      [trigKey('csc'), trigKey('sec'), trigKey('cot'), expKey, lnKey, derivKey, intKey, backspaceKey],
      [trigKey('sinh'), trigKey('cosh'), trigKey('tanh'), gammaKey, betaKey, xKey, leftKey, rightKey]
    ]
  },
  'beta-lower-english': betaEnglish(false),
  'beta-upper-english': betaEnglish(true),
  'beta-lower-greek': betaGreek(false),
  'beta-upper-greek': betaGreek(true)
}

const betaKeyboard = {
  'beta-basic': {
    label: '123',
    classes: 'tex-math',
    layer: 'beta-basic'
  },
  'beta-math': {
    label: 'f(x)',
    classes: 'tex-math',
    layer: 'beta-math'
  },
  'beta-english': {
    label: 'abc',
    classes: 'tex-math',
    layer: 'beta-lower-english',
    layers: ['beta-lower-english', 'beta-upper-english']
  },
  'beta-greek': {
    label: '&alpha;&beta;&gamma;',
    classes: 'tex-math',
    layer: 'beta-lower-greek',
    layers: ['beta-lower-greek', 'beta-upper-greek']
  }
}

const mathlive = ref()
const mfe = new MathfieldElement({
  fontsDirectory: '/fonts',
  customVirtualKeyboardLayers: betaKeyboardLayer,
  customVirtualKeyboards: betaKeyboard,
  virtualKeyboards: 'beta-basic beta-math beta-english beta-greek',
  virtualKeyboardMode: 'onfocus'
})

onMounted(() => {
  mfe.style = 'outline: transparent'
  const inlineShortcuts = mfe.getOption('inlineShortcuts')
  // disable non-standard LaTex shortcuts
  for (const key of ['dt', 'dx', 'dy', 'dz', 'ee']) {
    delete inlineShortcuts[key]
  }
  mfe.setOptions({ inlineShortcuts })
  mfe.addEventListener('input', event => {
    if (event.inputType === 'insertLineBreak') {
      mfe.blur()
      props.enterCallback()
    } else {
      props.inputCallback(mfe.value)
    }
  })
  mathlive.value.appendChild(mfe)
})

watchEffect(() => {
  // avoid typing x^1 <- 2 shows x^1 2 due to reset
  if (mfe.value !== props.input) {
    mfe.value = props.input
  }
})
</script>

<template>
  <n-card>
    <template #header>
      <n-a
        href="https://cortexjs.io/mathlive/"
        target="_blank"
        style="text-decoration: none;"
      >
        MathLive
      </n-a>
    </template>
    <n-scrollbar x-scrollable>
      <div ref="mathlive" />
    </n-scrollbar>
  </n-card>
</template>
