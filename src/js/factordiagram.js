// http://mathlesstraveled.com/2012/10/05/factorization-diagrams/
function FactorDiagram (primes, container) {
  this._primes = primes
  this._svg = d3.select(container)
  this._defs = this._svg.append('svg:defs')
  this._defs.append('circle')
    .attr('id', 'c')
    .attr('r', 2)
}

const translate = (x, y) => 'translate(' + x + ',' + y + ')'

FactorDiagram.prototype._dimensions = function (id) {
  const el = this._svg.append('use').attr('xlink:href', id)
  const bbox = el[0][0].getBBox()
  el.remove()
  return bbox
}

FactorDiagram.prototype.primeLayout = function (n, id, g) {
  const dims = this._dimensions(id)
  const w = dims.width
  const h = dims.height

  if (n === 1) {
    g.append('svg:g')
      .append('circle')
      .attr('r', 2)
  } else if (n === 2) {
    if (w > h) {
      g.append('svg:g')
        .append('svg:use')
        .attr('xlink:href', id)
        .attr('transform', translate(0, -h / 2))
      g.append('svg:g').attr('transform', translate(0, h))
        .append('svg:use')
        .attr('xlink:href', id)
    } else {
      g.append('svg:g')
        .append('svg:use')
        .attr('xlink:href', id)
        .attr('transform', translate(-w / 2, 0))
      g.append('svg:g').attr('transform', translate(w, 0))
        .append('svg:use')
        .attr('xlink:href', id)
    }
  } else {
    for (let i = 0; i < n; i++) {
      let m = d3.max([w, h])
      m = m * 0.75 / Math.sin((2 * Math.PI) / (2 * n))
      let alpha = i * (2 * Math.PI / n)
      alpha -= Math.PI / 2
      const x = m * Math.cos(alpha)
      const y = m * Math.sin(alpha)
      g.append('svg:g')
        .append('svg:use')
        .attr('xlink:href', id)
        .attr('transform', translate(x, y))
    }
  }
}

FactorDiagram.prototype.draw = function () {
  const factorDiagram = function (primes, num) {
    if (primes.length === 0) {
      return '#c'
    } else {
      const p = primes[0]
      const rest = primes.slice(1)
      const g = this._defs.append('svg:g').attr('id', 'g' + num)
      const next = factorDiagram.call(this, rest, num + 1)
      this.primeLayout(p, next, g, 2, 2)
      return '#' + g.attr('id')
    }
  }
  const diagram = factorDiagram.call(this, this._primes, 0)
  const el = this._svg.append('svg:use')
    .attr('xlink:href', diagram)
    .attr('id', 'diagram')
  const d = this._dimensions('#diagram')
  el.attr('transform', translate(-d.x, -d.y))
  this._svg.attr('width', d.width)
  this._svg.attr('height', d.height)
}

export { FactorDiagram }
