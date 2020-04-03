import React from 'react';
import '../scss/RefreshButton.scss';

class RefreshButton extends React.Component{
    refreshPage() {
        window.location.reload(false);
      }

    render () {
        return (
            <button onClick={this.refreshPage}>{this.props.children}</button>
        )
    }
}

export default RefreshButton;


