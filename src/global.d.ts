import { darkTheme } from 'naive-ui'

declare global {
  const d3: any

  type GlobalTheme = typeof darkTheme | null

  type SubCategory = {
    name?: string
    examples: {
      name?: string
      html?: true
      expression: string
    }[]
  }

  type Category = {
    name: string
    subCategories: SubCategory[]
  }

  type ErrorResult = {
    title?: string
    error: string
  }

  type AmbiguityCard = {
    ambiguity: string
    description: any[]
  }
  type ResultCard = {
    title: string
    input?: string
    output: Content
  }
  type MultiVarCard = ResultCard & {
    variables: string[]
    variable: string
  }
  type ContentCard = {
    name: string
    title: string
    input: string
    variable?: string
    pre_output?: string
    parameters?: string[]
  }
  type SourceContentCard = ContentCard & {
    source: string
  }
  type WikiContentCard = ContentCard & {
    wiki: string
  }
  type PlotCard = {
    title: string
    input: any[]
  }
  type InputResult = ErrorResult | ResultCard | MultiVarCard | AmbiguityCard | ContentCard | SourceContentCard | WikiContentCard | PlotCard

  type Content = {
    type: string
  } & (
    TexContent |
    ChineseNumeralContent |
    DocumentContent |
    ReferenceContent |
    TableContent |
    TruthTableContent |
    ListContent |
    FactorDiagramContent |
    PlotContent |
    TextContent |
    SvgContent |
    ContinuedFractionContent |
    MultiResultContent |
    StepContainerContent
  )

  type CardResult = ErrorResult | Content

  type TexContent = {
    tex: string
    numeric?: boolean
    expression?: string
    approximation?: string
  }
  type ChineseNumeralContent = {
    normal: string
    financial: string
  }
  type DocumentContent = {
    html: string
  }
  type ReferenceContent = {
    links: string[]
  }
  type TableContent = {
    titles: string[]
    rows: (string | Tex)[][]
  }
  type TruthTableContent = {
    titles: string[]
    rows: string[][]
  }
  type ListContent = {
    list: Content[]
  }
  type FactorDiagramContent = {
    primes: number[]
  }
  type PlotContent = {
    variable: string
    graphs: {
      function: string
      points: {
        x: number[]
        y: number[]
      }
    }[]
  }
  type TextContent = {
    text: string
  }
  type SvgContent = {
    svg: string
    category: string
  }
  type ContinuedFractionContent = {
    n: number
    finite: number[]
    repeated: number[] | undefined
  }
  type MultiResultContent = {
    results: {
      input: string
      output: Content
    }[]
  }
  type Step = {
    level?: Step[]
    step?: Step[]
    p?: Step[]
    collapsible?: Step[]
    text?: string
    inline?: string
    block?: string
    header?: string
  }
  type StepContainerContent = {
    content: Step
    answer: Step
  }
}
