import { useBreakpoint, useMemo } from 'vooks'

const isMobile = (() => {
  const breakpointRef = useBreakpoint()
  return useMemo(() => {
    return breakpointRef.value === 'xs'
  })
})() // copied from naive-ui (MIT)

export { isMobile }
