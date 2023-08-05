function GetOciTopLevelCommand_jms() {
    return 'jms'
}

function GetOciSubcommands_jms() {
    $ociSubcommands = @{
        'jms' = 'application-usage blocklist fleet fleet-agent-configuration installation-site-summary installation-usage jre-usage managed-instance-usage work-item-summary work-request work-request-error work-request-log-entry'
        'jms application-usage' = 'summarize'
        'jms blocklist' = 'create delete list'
        'jms fleet' = 'change-compartment create delete get list summarize-resource-inventory update'
        'jms fleet-agent-configuration' = 'get update'
        'jms installation-site-summary' = 'list-installation-sites remove'
        'jms installation-usage' = 'summarize'
        'jms jre-usage' = 'list summarize'
        'jms managed-instance-usage' = 'summarize'
        'jms work-item-summary' = 'list-work-items'
        'jms work-request' = 'cancel get list'
        'jms work-request-error' = 'list'
        'jms work-request-log-entry' = 'list-work-request-logs'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_jms() {
    $ociCommandsToLongParams = @{
        'jms application-usage summarize' = 'application-id application-type display-name fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id os-family page sort-by sort-order time-end time-start'
        'jms blocklist create' = 'fleet-id from-json help operation reason target'
        'jms blocklist delete' = 'blocklist-key fleet-id force from-json help if-match'
        'jms blocklist list' = 'all fleet-id from-json help limit managed-instance-id operation page page-size sort-by sort-order'
        'jms fleet change-compartment' = 'compartment-id fleet-id from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet create' = 'compartment-id defined-tags description display-name freeform-tags from-json help inventory-log max-wait-seconds operation-log wait-for-state wait-interval-seconds'
        'jms fleet delete' = 'fleet-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'jms fleet get' = 'fleet-id from-json help'
        'jms fleet list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'jms fleet summarize-resource-inventory' = 'compartment-id from-json help time-end time-start'
        'jms fleet update' = 'defined-tags description display-name fleet-id force freeform-tags from-json help if-match inventory-log max-wait-seconds operation-log wait-for-state wait-interval-seconds'
        'jms fleet-agent-configuration get' = 'fleet-id from-json help'
        'jms fleet-agent-configuration update' = 'fleet-id force from-json help if-match jre-scan-frequency jut-processing-frequency linux-configuration max-wait-seconds wait-for-state wait-interval-seconds windows-configuration'
        'jms installation-site-summary list-installation-sites' = 'all application-id fleet-id from-json help installation-path jre-distribution jre-security-status jre-vendor jre-version limit managed-instance-id os-family page page-size sort-by sort-order'
        'jms installation-site-summary remove' = 'fleet-id from-json help if-match installation-sites max-wait-seconds wait-for-state wait-interval-seconds'
        'jms installation-usage summarize' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id os-family page sort-by sort-order time-end time-start'
        'jms jre-usage list' = 'all application-id application-name compartment-id from-json help host-id limit page page-size sort-by sort-order time-end time-start'
        'jms jre-usage summarize' = 'application-id fields fleet-id from-json help jre-distribution jre-security-status jre-vendor jre-version limit managed-instance-id os-family page sort-by sort-order time-end time-start'
        'jms managed-instance-usage summarize' = 'application-id fields fleet-id from-json help installation-path jre-distribution jre-vendor jre-version limit managed-instance-id managed-instance-type os-family page sort-by sort-order time-end time-start'
        'jms work-item-summary list-work-items' = 'all from-json help limit page page-size work-request-id'
        'jms work-request cancel' = 'force from-json help if-match work-request-id'
        'jms work-request get' = 'from-json help work-request-id'
        'jms work-request list' = 'all compartment-id fleet-id from-json help id limit page page-size'
        'jms work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'jms work-request-log-entry list-work-request-logs' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_jms() {
    $ociCommandsToShortParams = @{
        'jms application-usage summarize' = '? h'
        'jms blocklist create' = '? h'
        'jms blocklist delete' = '? h'
        'jms blocklist list' = '? h'
        'jms fleet change-compartment' = '? c h'
        'jms fleet create' = '? c h'
        'jms fleet delete' = '? h'
        'jms fleet get' = '? h'
        'jms fleet list' = '? c h'
        'jms fleet summarize-resource-inventory' = '? c h'
        'jms fleet update' = '? h'
        'jms fleet-agent-configuration get' = '? h'
        'jms fleet-agent-configuration update' = '? h'
        'jms installation-site-summary list-installation-sites' = '? h'
        'jms installation-site-summary remove' = '? h'
        'jms installation-usage summarize' = '? h'
        'jms jre-usage list' = '? c h'
        'jms jre-usage summarize' = '? h'
        'jms managed-instance-usage summarize' = '? h'
        'jms work-item-summary list-work-items' = '? h'
        'jms work-request cancel' = '? h'
        'jms work-request get' = '? h'
        'jms work-request list' = '? c h'
        'jms work-request-error list' = '? h'
        'jms work-request-log-entry list-work-request-logs' = '? h'
    }
    return $ociCommandsToShortParams
}