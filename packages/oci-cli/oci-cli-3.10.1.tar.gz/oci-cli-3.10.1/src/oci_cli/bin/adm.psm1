function GetOciTopLevelCommand_adm() {
    return 'adm'
}

function GetOciSubcommands_adm() {
    $ociSubcommands = @{
        'adm' = 'knowledge-base vulnerability-audit work-request work-request-error work-request-log-entry'
        'adm knowledge-base' = 'change-compartment create delete get list update'
        'adm vulnerability-audit' = 'change-compartment create delete get list list-application-dependency-vulnerabilities update'
        'adm work-request' = 'cancel get list'
        'adm work-request-error' = 'list'
        'adm work-request-log-entry' = 'list-work-request-logs'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_adm() {
    $ociCommandsToLongParams = @{
        'adm knowledge-base change-compartment' = 'compartment-id from-json help if-match knowledge-base-id max-wait-seconds wait-for-state wait-interval-seconds'
        'adm knowledge-base create' = 'compartment-id defined-tags display-name freeform-tags from-json help max-wait-seconds wait-for-state wait-interval-seconds'
        'adm knowledge-base delete' = 'force from-json help if-match knowledge-base-id max-wait-seconds wait-for-state wait-interval-seconds'
        'adm knowledge-base get' = 'from-json help knowledge-base-id'
        'adm knowledge-base list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'adm knowledge-base update' = 'defined-tags display-name force freeform-tags from-json help if-match knowledge-base-id max-wait-seconds wait-for-state wait-interval-seconds'
        'adm vulnerability-audit change-compartment' = 'compartment-id from-json help if-match vulnerability-audit-id'
        'adm vulnerability-audit create' = 'application-dependencies build-type compartment-id configuration defined-tags display-name freeform-tags from-json help if-match knowledge-base-id max-wait-seconds wait-for-state wait-interval-seconds'
        'adm vulnerability-audit delete' = 'force from-json help if-match max-wait-seconds vulnerability-audit-id wait-for-state wait-interval-seconds'
        'adm vulnerability-audit get' = 'from-json help vulnerability-audit-id'
        'adm vulnerability-audit list' = 'all compartment-id display-name from-json help id is-success knowledge-base-id lifecycle-state limit page page-size sort-by sort-order'
        'adm vulnerability-audit list-application-dependency-vulnerabilities' = 'all cvss-v2-greater-than-or-equal cvss-v3-greater-than-or-equal from-json gav help limit page page-size sort-by sort-order vulnerability-audit-id vulnerability-id'
        'adm vulnerability-audit update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds vulnerability-audit-id wait-for-state wait-interval-seconds'
        'adm work-request cancel' = 'force from-json help if-match work-request-id'
        'adm work-request get' = 'from-json help work-request-id'
        'adm work-request list' = 'all compartment-id from-json help limit page page-size resource-id sort-by sort-order status work-request-id'
        'adm work-request-error list' = 'all from-json help limit page page-size sort-by sort-order work-request-id'
        'adm work-request-log-entry list-work-request-logs' = 'all from-json help limit page page-size sort-by sort-order work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_adm() {
    $ociCommandsToShortParams = @{
        'adm knowledge-base change-compartment' = '? c h'
        'adm knowledge-base create' = '? c h'
        'adm knowledge-base delete' = '? h'
        'adm knowledge-base get' = '? h'
        'adm knowledge-base list' = '? c h'
        'adm knowledge-base update' = '? h'
        'adm vulnerability-audit change-compartment' = '? c h'
        'adm vulnerability-audit create' = '? c h'
        'adm vulnerability-audit delete' = '? h'
        'adm vulnerability-audit get' = '? h'
        'adm vulnerability-audit list' = '? c h'
        'adm vulnerability-audit list-application-dependency-vulnerabilities' = '? h'
        'adm vulnerability-audit update' = '? h'
        'adm work-request cancel' = '? h'
        'adm work-request get' = '? h'
        'adm work-request list' = '? c h'
        'adm work-request-error list' = '? h'
        'adm work-request-log-entry list-work-request-logs' = '? h'
    }
    return $ociCommandsToShortParams
}