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
	timeout has a value which is an int
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
	timeout has a value which is an int
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
	timeout has a value which is an int
	verify_ssl has a value which is an UIService.Boolean
Boolean is an int
CheckImageURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
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
	timeout has a value which is an int
	verify_ssl has a value which is an UIService.Boolean
Boolean is an int
CheckImageURLResult is a reference to a hash where the following keys are defined:
	is_valid has a value which is an UIService.Boolean
	error has a value which is an UIService.CheckError
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



=head2 CheckError

=over 4



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
timeout has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
url has a value which is a string
timeout has a value which is an int


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
timeout has a value which is an int
verify_ssl has a value which is an UIService.Boolean

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
url has a value which is a string
timeout has a value which is an int
verify_ssl has a value which is an UIService.Boolean


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
