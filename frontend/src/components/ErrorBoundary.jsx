import React from 'react'
import { Alert } from '@mui/material'

/**
 * Catches JavaScript errors inside one dashboard panel so a chart crash
 * never takes down the whole dashboard. Each panel is wrapped individually.
 */
export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error, info) {
    // eslint-disable-next-line no-console
    console.error('Panel error:', error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <Alert severity="error" variant="outlined">
          {this.props.label || 'Panel'} failed to render: {String(this.state.error.message || this.state.error)}
        </Alert>
      )
    }
    return this.props.children
  }
}
