export function ResubmitController($scope, $http, $location, $timeout) {

    $scope.error = false
    $scope.loading = false
    $scope.done = false
    $scope.resubmit = function(test_job_id, force) {
        if ($scope.done) return
        $scope.loading = true

        var endpoint = force ? "/force_resubmit/" : "/resubmit/";

        $http.post("/api/testjobs/" + test_job_id + endpoint).then(
            function(response) {
                $timeout(function() {
                    $scope.loading = false
                    $scope.done = true
                }, 1000)
            },
            function(response) {
                var msg = "There was an error while resubmitting.\n" +
                    "Status = " + response.status + " " + response.statusText +
                    "(" + response.xhrStatus + ")"
                alert(msg)
                $scope.loading = false
                $scope.error = true
                $scope.done = true
            }
        )
    }
}
