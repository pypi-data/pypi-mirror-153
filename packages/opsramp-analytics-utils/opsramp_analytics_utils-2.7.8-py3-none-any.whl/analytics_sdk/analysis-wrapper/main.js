// generate the proper entry point structure
var AnalyticsAppsUIEntry = document.getElementById('AnalyticsAppsUI-container');
var innerStartEntryHtml = `
<div class="d-flex">
    <div class="sidebar d-print-none">
        <div id="AnalyticsAppsUI-sidebar-container" class="h-100"></div>
    </div>
    <div class="analysis-content" style="flex: 1;">
        <div id="AnalyticsAppsUI-report-container">
            <div class="_dash-loading">
                Loading...
            </div>
        </div>
    </div>
</div>
`;

AnalyticsAppsUIEntry.insertAdjacentHTML('beforeend', innerStartEntryHtml);

// load the real main js
var rootReportScript = document.currentScript,
    rootReportScriptUrl = rootReportScript.getAttribute('src'),
    mainReportScript = document.createElement('script');

mainReportScript.src = rootReportScriptUrl.replace('main.js', 'report_main.js');
document.head.appendChild(mainReportScript);
