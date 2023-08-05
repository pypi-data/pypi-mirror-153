function GetOciTopLevelCommand_usage() {
    return 'usage'
}

function GetOciSubcommands_usage() {
    $ociSubcommands = @{
        'usage' = 'monthly-reward-summary product-summary redeemable-user redeemable-user-summary'
        'usage monthly-reward-summary' = 'list-rewards'
        'usage product-summary' = 'list-products'
        'usage redeemable-user' = 'create delete'
        'usage redeemable-user-summary' = 'list-redeemable-users'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_usage() {
    $ociCommandsToLongParams = @{
        'usage monthly-reward-summary list-rewards' = 'all from-json help subscription-id tenancy-id'
        'usage product-summary list-products' = 'all from-json help limit page page-size producttype sort-by sort-order subscription-id tenancy-id usage-period-key'
        'usage redeemable-user create' = 'from-json help if-match items subscription-id tenancy-id user-id'
        'usage redeemable-user delete' = 'email-id force from-json help if-match subscription-id tenancy-id'
        'usage redeemable-user-summary list-redeemable-users' = 'all from-json help limit page page-size sort-by sort-order subscription-id tenancy-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_usage() {
    $ociCommandsToShortParams = @{
        'usage monthly-reward-summary list-rewards' = '? h'
        'usage product-summary list-products' = '? h'
        'usage redeemable-user create' = '? h'
        'usage redeemable-user delete' = '? h'
        'usage redeemable-user-summary list-redeemable-users' = '? h'
    }
    return $ociCommandsToShortParams
}