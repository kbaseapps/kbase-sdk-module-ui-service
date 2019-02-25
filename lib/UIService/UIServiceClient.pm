package UIService::UIServiceClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

UIService::UIServiceClient

=head1 DESCRIPTION


A KBase module: UIService


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => UIService::UIServiceClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 get_alert

  $alert, $error = $obj->get_alert($param)

=over 4

=item Parameter and return types

=begin html

<pre>
$param is an UIService.GetAlertParam
$alert is an UIService.Alert
$error is an UIService.Error
GetAlertParam is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
AlertID is a string
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$param is an UIService.GetAlertParam
$alert is an UIService.Alert
$error is an UIService.Error
GetAlertParam is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
AlertID is a string
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub get_alert
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_alert (received $n, expecting 1)");
    }
    {
	my($param) = @args;

	my @_bad_arguments;
        (ref($param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"param\" (value was \"$param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_alert:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_alert');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.get_alert",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_alert',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_alert",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_alert',
				       );
    }
}
 


=head2 get_active_alerts

  $alerts, $error = $obj->get_active_alerts()

=over 4

=item Parameter and return types

=begin html

<pre>
$alerts is a reference to a list where each element is an UIService.Alert
$error is an UIService.Error
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$alerts is a reference to a list where each element is an UIService.Alert
$error is an UIService.Error
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description

get_active_alerts

=back

=cut

 sub get_active_alerts
{
    my($self, @args) = @_;

# Authentication: optional

    if ((my $n = @args) != 0)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_active_alerts (received $n, expecting 0)");
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.get_active_alerts",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_active_alerts',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_active_alerts",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_active_alerts',
				       );
    }
}
 


=head2 search_alerts

  $result, $error = $obj->search_alerts($query)

=over 4

=item Parameter and return types

=begin html

<pre>
$query is an UIService.AlertQuery
$result is an UIService.SearchAlertsResult
$error is an UIService.Error
AlertQuery is a reference to a hash where the following keys are defined:
	query has a value which is an UIService.SearchExpression
	paging has a value which is an UIService.PagingSpec
	sorting has a value which is a reference to a list where each element is an UIService.SortSpec
SearchExpression is an UnspecifiedObject, which can hold any non-null object
PagingSpec is a reference to a hash where the following keys are defined:
	start has a value which is an int
	limit has a value which is an int
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	is_descending has a value which is an UIService.Boolean
Boolean is an int
SearchAlertsResult is a reference to a hash where the following keys are defined:
	alerts has a value which is a reference to a list where each element is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$query is an UIService.AlertQuery
$result is an UIService.SearchAlertsResult
$error is an UIService.Error
AlertQuery is a reference to a hash where the following keys are defined:
	query has a value which is an UIService.SearchExpression
	paging has a value which is an UIService.PagingSpec
	sorting has a value which is a reference to a list where each element is an UIService.SortSpec
SearchExpression is an UnspecifiedObject, which can hold any non-null object
PagingSpec is a reference to a hash where the following keys are defined:
	start has a value which is an int
	limit has a value which is an int
SortSpec is a reference to a hash where the following keys are defined:
	field has a value which is a string
	is_descending has a value which is an UIService.Boolean
Boolean is an int
SearchAlertsResult is a reference to a hash where the following keys are defined:
	alerts has a value which is a reference to a list where each element is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub search_alerts
{
    my($self, @args) = @_;

# Authentication: none

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function search_alerts (received $n, expecting 1)");
    }
    {
	my($query) = @args;

	my @_bad_arguments;
        (ref($query) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"query\" (value was \"$query\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to search_alerts:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'search_alerts');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.search_alerts",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'search_alerts',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method search_alerts",
					    status_line => $self->{client}->status_line,
					    method_name => 'search_alerts',
				       );
    }
}
 


=head2 search_alerts_summary

  $result, $error = $obj->search_alerts_summary($query)

=over 4

=item Parameter and return types

=begin html

<pre>
$query is an UIService.SearchExpression
$result is an UIService.SearchAlertsSummaryResult
$error is an UIService.Error
SearchExpression is an UnspecifiedObject, which can hold any non-null object
SearchAlertsSummaryResult is a reference to a hash where the following keys are defined:
	statuses has a value which is a reference to a hash where the key is a string and the value is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$query is an UIService.SearchExpression
$result is an UIService.SearchAlertsSummaryResult
$error is an UIService.Error
SearchExpression is an UnspecifiedObject, which can hold any non-null object
SearchAlertsSummaryResult is a reference to a hash where the following keys are defined:
	statuses has a value which is a reference to a hash where the key is a string and the value is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub search_alerts_summary
{
    my($self, @args) = @_;

# Authentication: none

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function search_alerts_summary (received $n, expecting 1)");
    }
    {
	my($query) = @args;

	my @_bad_arguments;
        (defined $query) or push(@_bad_arguments, "Invalid type for argument 1 \"query\" (value was \"$query\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to search_alerts_summary:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'search_alerts_summary');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.search_alerts_summary",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'search_alerts_summary',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method search_alerts_summary",
					    status_line => $self->{client}->status_line,
					    method_name => 'search_alerts_summary',
				       );
    }
}
 


=head2 am_admin_user

  $is_admin, $error = $obj->am_admin_user()

=over 4

=item Parameter and return types

=begin html

<pre>
$is_admin is an UIService.Boolean
$error is an UIService.Error
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$is_admin is an UIService.Boolean
$error is an UIService.Error
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description

am_admin_user

=back

=cut

 sub am_admin_user
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 0)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function am_admin_user (received $n, expecting 0)");
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.am_admin_user",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'am_admin_user',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method am_admin_user",
					    status_line => $self->{client}->status_line,
					    method_name => 'am_admin_user',
				       );
    }
}
 


=head2 add_alert

  $result, $error = $obj->add_alert($alert_param)

=over 4

=item Parameter and return types

=begin html

<pre>
$alert_param is an UIService.AddAlertParam
$result is an UIService.AddAlertResult
$error is an UIService.Error
AddAlertParam is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
AddAlertResult is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$alert_param is an UIService.AddAlertParam
$result is an UIService.AddAlertResult
$error is an UIService.Error
AddAlertParam is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
AddAlertResult is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub add_alert
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function add_alert (received $n, expecting 1)");
    }
    {
	my($alert_param) = @args;

	my @_bad_arguments;
        (ref($alert_param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"alert_param\" (value was \"$alert_param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to add_alert:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'add_alert');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.add_alert",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'add_alert',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method add_alert",
					    status_line => $self->{client}->status_line,
					    method_name => 'add_alert',
				       );
    }
}
 


=head2 delete_alert

  $result, $error = $obj->delete_alert($id)

=over 4

=item Parameter and return types

=begin html

<pre>
$id is an UIService.AlertID
$result is an UIService.DeleteAlertResult
$error is an UIService.Error
AlertID is a string
DeleteAlertResult is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$id is an UIService.AlertID
$result is an UIService.DeleteAlertResult
$error is an UIService.Error
AlertID is a string
DeleteAlertResult is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub delete_alert
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function delete_alert (received $n, expecting 1)");
    }
    {
	my($id) = @args;

	my @_bad_arguments;
        (!ref($id)) or push(@_bad_arguments, "Invalid type for argument 1 \"id\" (value was \"$id\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to delete_alert:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'delete_alert');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.delete_alert",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'delete_alert',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method delete_alert",
					    status_line => $self->{client}->status_line,
					    method_name => 'delete_alert',
				       );
    }
}
 


=head2 is_admin_user

  $is_admin, $error = $obj->is_admin_user($param)

=over 4

=item Parameter and return types

=begin html

<pre>
$param is an UIService.IsAdminUserParam
$is_admin is an UIService.Boolean
$error is an UIService.Error
IsAdminUserParam is a reference to a hash where the following keys are defined:
	username has a value which is an UIService.Username
Username is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$param is an UIService.IsAdminUserParam
$is_admin is an UIService.Boolean
$error is an UIService.Error
IsAdminUserParam is a reference to a hash where the following keys are defined:
	username has a value which is an UIService.Username
Username is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub is_admin_user
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function is_admin_user (received $n, expecting 1)");
    }
    {
	my($param) = @args;

	my @_bad_arguments;
        (ref($param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"param\" (value was \"$param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to is_admin_user:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'is_admin_user');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.is_admin_user",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'is_admin_user',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method is_admin_user",
					    status_line => $self->{client}->status_line,
					    method_name => 'is_admin_user',
				       );
    }
}
 


=head2 update_alert

  $success, $error = $obj->update_alert($alert_param)

=over 4

=item Parameter and return types

=begin html

<pre>
$alert_param is an UIService.UpdateAlertParams
$success is an UIService.Boolean
$error is an UIService.Error
UpdateAlertParams is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$alert_param is an UIService.UpdateAlertParams
$success is an UIService.Boolean
$error is an UIService.Error
UpdateAlertParams is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub update_alert
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function update_alert (received $n, expecting 1)");
    }
    {
	my($alert_param) = @args;

	my @_bad_arguments;
        (ref($alert_param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"alert_param\" (value was \"$alert_param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to update_alert:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'update_alert');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.update_alert",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'update_alert',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method update_alert",
					    status_line => $self->{client}->status_line,
					    method_name => 'update_alert',
				       );
    }
}
 


=head2 set_alert

  $success, $error = $obj->set_alert($alert_param)

=over 4

=item Parameter and return types

=begin html

<pre>
$alert_param is an UIService.UpdateAlertParams
$success is an UIService.Boolean
$error is an UIService.Error
UpdateAlertParams is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$alert_param is an UIService.UpdateAlertParams
$success is an UIService.Boolean
$error is an UIService.Error
UpdateAlertParams is a reference to a hash where the following keys are defined:
	alert has a value which is an UIService.Alert
Alert is a reference to a hash where the following keys are defined:
	id has a value which is an UIService.AlertID
	start_at has a value which is an UIService.Timestamp
	end_at has a value which is an UIService.Timestamp
	type has a value which is an UIService.AlertType
	title has a value which is a string
	message has a value which is a string
	status has a value which is an UIService.AlertStatus
	created_at has a value which is an UIService.Timestamp
	created_by has a value which is a string
	updated_at has a value which is an UIService.Timestamp
	updated_by has a value which is a string
AlertID is a string
Timestamp is an int
AlertType is a string
AlertStatus is a string
Boolean is an int
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub set_alert
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function set_alert (received $n, expecting 1)");
    }
    {
	my($alert_param) = @args;

	my @_bad_arguments;
        (ref($alert_param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"alert_param\" (value was \"$alert_param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to set_alert:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'set_alert');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.set_alert",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'set_alert',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method set_alert",
					    status_line => $self->{client}->status_line,
					    method_name => 'set_alert',
				       );
    }
}
 


=head2 check_html_url

  $result, $error = $obj->check_html_url($param)

=over 4

=item Parameter and return types

=begin html

<pre>
$param is an UIService.CheckHTMLURLParams
$result is an UIService.CheckHTMLURLResult
$error is an UIService.Error
CheckHTMLURLParams is a reference to a hash where the following keys are defined:
	url has a value which is a string
CheckHTMLURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
Boolean is an int
CheckError is a reference to a hash where the following keys are defined:
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$param is an UIService.CheckHTMLURLParams
$result is an UIService.CheckHTMLURLResult
$error is an UIService.Error
CheckHTMLURLParams is a reference to a hash where the following keys are defined:
	url has a value which is a string
CheckHTMLURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
Boolean is an int
CheckError is a reference to a hash where the following keys are defined:
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub check_html_url
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function check_html_url (received $n, expecting 1)");
    }
    {
	my($param) = @args;

	my @_bad_arguments;
        (ref($param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"param\" (value was \"$param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to check_html_url:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'check_html_url');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.check_html_url",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'check_html_url',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method check_html_url",
					    status_line => $self->{client}->status_line,
					    method_name => 'check_html_url',
				       );
    }
}
 


=head2 check_image_url

  $result, $error = $obj->check_image_url($param)

=over 4

=item Parameter and return types

=begin html

<pre>
$param is an UIService.CheckImageURLParams
$result is an UIService.CheckImageURLResult
$error is an UIService.Error
CheckImageURLParams is a reference to a hash where the following keys are defined:
	url has a value which is a string
CheckImageURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
Boolean is an int
CheckError is a reference to a hash where the following keys are defined:
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

$param is an UIService.CheckImageURLParams
$result is an UIService.CheckImageURLResult
$error is an UIService.Error
CheckImageURLParams is a reference to a hash where the following keys are defined:
	url has a value which is a string
CheckImageURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
Boolean is an int
CheckError is a reference to a hash where the following keys are defined:
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object
Error is a reference to a hash where the following keys are defined:
	message has a value which is a string
	type has a value which is a string
	code has a value which is a string
	info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=item Description



=back

=cut

 sub check_image_url
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function check_image_url (received $n, expecting 1)");
    }
    {
	my($param) = @args;

	my @_bad_arguments;
        (ref($param) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"param\" (value was \"$param\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to check_image_url:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'check_image_url');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "UIService.check_image_url",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'check_image_url',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method check_image_url",
					    status_line => $self->{client}->status_line,
					    method_name => 'check_image_url',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "UIService.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "UIService.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'check_image_url',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method check_image_url",
            status_line => $self->{client}->status_line,
            method_name => 'check_image_url',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for UIService::UIServiceClient\n";
    }
    if ($sMajor == 0) {
        warn "UIService::UIServiceClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 Timestamp

=over 4



=item Description

BASE Types


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 AlertStatus

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 AlertType

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 AlertID

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 Username

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 Boolean

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 Alert

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID
start_at has a value which is an UIService.Timestamp
end_at has a value which is an UIService.Timestamp
type has a value which is an UIService.AlertType
title has a value which is a string
message has a value which is a string
status has a value which is an UIService.AlertStatus
created_at has a value which is an UIService.Timestamp
created_by has a value which is a string
updated_at has a value which is an UIService.Timestamp
updated_by has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID
start_at has a value which is an UIService.Timestamp
end_at has a value which is an UIService.Timestamp
type has a value which is an UIService.AlertType
title has a value which is a string
message has a value which is a string
status has a value which is an UIService.AlertStatus
created_at has a value which is an UIService.Timestamp
created_by has a value which is a string
updated_at has a value which is an UIService.Timestamp
updated_by has a value which is a string


=end text

=back



=head2 Error

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
message has a value which is a string
type has a value which is a string
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
message has a value which is a string
type has a value which is a string
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=back



=head2 GetAlertParam

=over 4



=item Description

get_alert


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID


=end text

=back



=head2 PagingSpec

=over 4



=item Description

search_alerts


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
start has a value which is an int
limit has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
start has a value which is an int
limit has a value which is an int


=end text

=back



=head2 SortSpec

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
field has a value which is a string
is_descending has a value which is an UIService.Boolean

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
field has a value which is a string
is_descending has a value which is an UIService.Boolean


=end text

=back



=head2 SearchExpression

=over 4



=item Description

I give up ...


=item Definition

=begin html

<pre>
an UnspecifiedObject, which can hold any non-null object
</pre>

=end html

=begin text

an UnspecifiedObject, which can hold any non-null object

=end text

=back



=head2 AlertQuery

=over 4



=item Description

typedef structure {
    string path;        
    string op; 
    string value;
} SearchField;


typedef structure {
    string op;
    list<SearchField> args;
} SearchSubExpression;


typedef structure {
    SearchField field;
    SearchSubExpression expression;
} SearchArg;

typedef structure {
    string op;
    list<SearchArg> args;
} SearchExpression;


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
query has a value which is an UIService.SearchExpression
paging has a value which is an UIService.PagingSpec
sorting has a value which is a reference to a list where each element is an UIService.SortSpec

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
query has a value which is an UIService.SearchExpression
paging has a value which is an UIService.PagingSpec
sorting has a value which is a reference to a list where each element is an UIService.SortSpec


=end text

=back



=head2 SearchAlertsResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
alerts has a value which is a reference to a list where each element is an UIService.Alert

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
alerts has a value which is a reference to a list where each element is an UIService.Alert


=end text

=back



=head2 SearchAlertsSummaryResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
statuses has a value which is a reference to a hash where the key is a string and the value is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
statuses has a value which is a reference to a hash where the key is a string and the value is an int


=end text

=back



=head2 AddAlertParam

=over 4



=item Description

add_alert


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
alert has a value which is an UIService.Alert

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
alert has a value which is an UIService.Alert


=end text

=back



=head2 AddAlertResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID


=end text

=back



=head2 DeleteAlertResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
id has a value which is an UIService.AlertID


=end text

=back



=head2 IsAdminUserParam

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
username has a value which is an UIService.Username

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
username has a value which is an UIService.Username


=end text

=back



=head2 UpdateAlertParams

=over 4



=item Description

update alert


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
alert has a value which is an UIService.Alert

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
alert has a value which is an UIService.Alert


=end text

=back



=head2 CheckError

=over 4



=item Description

Validations


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
code has a value which is a string
info has a value which is an UnspecifiedObject, which can hold any non-null object


=end text

=back



=head2 CheckHTMLURLParams

=over 4



=item Description

Check html url


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
url has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
url has a value which is a string


=end text

=back



=head2 CheckHTMLURLResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
is_valid has a value which is an UIService.Boolean
error has a value which is an UIService.CheckError

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
is_valid has a value which is an UIService.Boolean
error has a value which is an UIService.CheckError


=end text

=back



=head2 CheckImageURLParams

=over 4



=item Description

Check image url


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
url has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
url has a value which is a string


=end text

=back



=head2 CheckImageURLResult

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
is_valid has a value which is an UIService.Boolean
error has a value which is an UIService.CheckError

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
is_valid has a value which is an UIService.Boolean
error has a value which is an UIService.CheckError


=end text

=back



=cut

package UIService::UIServiceClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
