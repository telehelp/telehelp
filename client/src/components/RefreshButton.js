import React from 'react';
import './RefreshButton.css';

function RefreshButton() {
    function refreshPage() {
        window.location.reload(false);
      }

    return (
        <div>
         <button onClick={refreshPage}>What's the current time now then?</button>
        </div>
    )
}

export default RefreshButton;


