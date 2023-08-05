function GetOciTopLevelCommand_rover() {
    return 'rover'
}

function GetOciSubcommands_rover() {
    $ociSubcommands = @{
        'rover' = 'create-master-key-policy node shape standalone-cluster station-cluster'
        'rover node' = 'add-workload change-compartment create delete delete-workload get-certificate get-encryption-key list list-workload request-approval set-secrets setup-identity show update'
        'rover shape' = 'list'
        'rover standalone-cluster' = 'add-workload change-compartment create delete delete-workload get-certificate list list-workloads request-approval set-secrets show update'
        'rover station-cluster' = 'add-workload change-compartment create delete delete-workload get-certificate list-workloads request-approval set-secrets show update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_rover() {
    $ociCommandsToLongParams = @{
        'rover create-master-key-policy' = 'help master-key-id policy-compartment-id policy-name'
        'rover node add-workload' = 'bucket-name force from-json help image-id node-id prefix range-end range-start type'
        'rover node change-compartment' = 'compartment-id from-json help if-match node-id'
        'rover node create' = 'address1 address2 address3 address4 addressee care-of city-or-locality compartment-id country defined-tags display-name email enclosure-type freeform-tags from-json help lifecycle-state lifecycle-state-details master-key-id max-wait-seconds phone-number point-of-contact point-of-contact-phone-number policy-compartment-id policy-name setup-identity shape shipping-preference state-province-region system-tags time-return-window-ends time-return-window-starts wait-for-state wait-interval-seconds zip-postal-code'
        'rover node delete' = 'force from-json help if-match max-wait-seconds node-id wait-for-state wait-interval-seconds'
        'rover node delete-workload' = 'force from-json help node-id'
        'rover node get-certificate' = 'from-json help node-id output-file-path'
        'rover node get-encryption-key' = 'from-json help node-id'
        'rover node list' = 'all compartment-id display-name from-json help lifecycle-state limit node-type page page-size shape sort-by sort-order'
        'rover node list-workload' = 'from-json help node-id'
        'rover node request-approval' = 'from-json help node-id'
        'rover node set-secrets' = 'from-json help node-id super-user-password unlock-passphrase'
        'rover node setup-identity' = 'from-json help node-id'
        'rover node show' = 'from-json help node-id'
        'rover node update' = 'address1 address2 address3 address4 addressee care-of city-or-locality country defined-tags display-name email enclosure-type force freeform-tags from-json help if-match lifecycle-state lifecycle-state-details max-wait-seconds node-id phone-number point-of-contact point-of-contact-phone-number shape shipping-preference state-province-region system-tags time-return-window-ends time-return-window-starts wait-for-state wait-interval-seconds zip-postal-code'
        'rover shape list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'rover standalone-cluster add-workload' = 'bucket-name cluster-id force from-json help image-id prefix range-end range-start type'
        'rover standalone-cluster change-compartment' = 'cluster-id compartment-id from-json help if-match'
        'rover standalone-cluster create' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-size cluster-type compartment-id country defined-tags display-name email enclosure-type freeform-tags from-json help lifecycle-state lifecycle-state-details master-key-id max-wait-seconds phone-number point-of-contact point-of-contact-phone-number policy-compartment-id policy-name shipping-preference state-province-region subscription-id system-tags wait-for-state wait-interval-seconds zip-postal-code'
        'rover standalone-cluster delete' = 'cluster-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'rover standalone-cluster delete-workload' = 'cluster-id force from-json help'
        'rover standalone-cluster get-certificate' = 'cluster-id from-json help output-file-path'
        'rover standalone-cluster list' = 'all cluster-type compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'rover standalone-cluster list-workloads' = 'cluster-id from-json help'
        'rover standalone-cluster request-approval' = 'cluster-id from-json help'
        'rover standalone-cluster set-secrets' = 'cluster-id help super-user-password unlock-passphrase'
        'rover standalone-cluster show' = 'cluster-id from-json help'
        'rover standalone-cluster update' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-id cluster-size country defined-tags display-name email enclosure-type force freeform-tags from-json help if-match lifecycle-state lifecycle-state-details max-wait-seconds phone-number point-of-contact point-of-contact-phone-number shipping-preference state-province-region subscription-id system-tags wait-for-state wait-interval-seconds zip-postal-code'
        'rover station-cluster add-workload' = 'bucket-name cluster-id force from-json help image-id prefix range-end range-start type'
        'rover station-cluster change-compartment' = 'cluster-id compartment-id from-json help if-match'
        'rover station-cluster create' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-size cluster-type compartment-id country data-validation-code defined-tags display-name email enclosure-type freeform-tags from-json help import-compartment-id import-file-bucket is-import-requested lifecycle-state lifecycle-state-details master-key-id max-wait-seconds phone-number point-of-contact point-of-contact-phone-number policy-compartment-id policy-name shipping-preference state-province-region subscription-id system-tags wait-for-state wait-interval-seconds zip-postal-code'
        'rover station-cluster delete' = 'cluster-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'rover station-cluster delete-workload' = 'cluster-id force from-json help'
        'rover station-cluster get-certificate' = 'cluster-id from-json help output-file-path'
        'rover station-cluster list-workloads' = 'cluster-id from-json help'
        'rover station-cluster request-approval' = 'cluster-id from-json help subscription-id'
        'rover station-cluster set-secrets' = 'cluster-id help super-user-password unlock-passphrase'
        'rover station-cluster show' = 'cluster-id from-json help'
        'rover station-cluster update' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-id cluster-size country data-validation-code defined-tags display-name email enclosure-type force freeform-tags from-json help if-match import-compartment-id import-file-bucket is-import-requested lifecycle-state lifecycle-state-details max-wait-seconds phone-number point-of-contact point-of-contact-phone-number shipping-preference state-province-region subscription-id system-tags wait-for-state wait-interval-seconds zip-postal-code'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_rover() {
    $ociCommandsToShortParams = @{
        'rover create-master-key-policy' = '? h'
        'rover node add-workload' = '? h'
        'rover node change-compartment' = '? c h'
        'rover node create' = '? c h'
        'rover node delete' = '? h'
        'rover node delete-workload' = '? h'
        'rover node get-certificate' = '? h'
        'rover node get-encryption-key' = '? h'
        'rover node list' = '? c h'
        'rover node list-workload' = '? h'
        'rover node request-approval' = '? h'
        'rover node set-secrets' = '? h'
        'rover node setup-identity' = '? h'
        'rover node show' = '? h'
        'rover node update' = '? h'
        'rover shape list' = '? c h'
        'rover standalone-cluster add-workload' = '? h'
        'rover standalone-cluster change-compartment' = '? c h'
        'rover standalone-cluster create' = '? c h'
        'rover standalone-cluster delete' = '? h'
        'rover standalone-cluster delete-workload' = '? h'
        'rover standalone-cluster get-certificate' = '? h'
        'rover standalone-cluster list' = '? c h'
        'rover standalone-cluster list-workloads' = '? h'
        'rover standalone-cluster request-approval' = '? h'
        'rover standalone-cluster set-secrets' = '? h'
        'rover standalone-cluster show' = '? h'
        'rover standalone-cluster update' = '? h'
        'rover station-cluster add-workload' = '? h'
        'rover station-cluster change-compartment' = '? c h'
        'rover station-cluster create' = '? c h'
        'rover station-cluster delete' = '? h'
        'rover station-cluster delete-workload' = '? h'
        'rover station-cluster get-certificate' = '? h'
        'rover station-cluster list-workloads' = '? h'
        'rover station-cluster request-approval' = '? h'
        'rover station-cluster set-secrets' = '? h'
        'rover station-cluster show' = '? h'
        'rover station-cluster update' = '? h'
    }
    return $ociCommandsToShortParams
}